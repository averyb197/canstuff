import subprocess
import json
import argparse
from tqdm import tqdm

#Default for ollama on our server, generally it 11434 tho
URL = "127.0.0.1:11438/api/generate"
NUM_PER_PROMPT = 1

task_instructs = ("You will be given 3 words, and you must write a very short story "
                  "that is 4 to 6 sentences long, that includes all 3 words. Try to use your imagination and be creative "
                  "when writing your story. The 3 words are: ")
prompt_words = [
    "stamp-letter-send",
    "petrol-diesel-pump",
    "year-week-embark",
    "statement-stealth-detect",
    "belief-faith-sing",
    "organ-empire-comply",
    "gloom-payment-exist"
]

# basically a .csv but round here we call it a .txt
def load_models(models_path):
    with open(models_path, "r") as feil:
        rawtxt = feil.read()
        models = rawtxt.split(",")
        return models


def make_prompts(instructions, wordlist, available_models):
    promptlist = []
    keylist = []
    for n in range(NUM_PER_PROMPT):
        for i in range(len(available_models)):
            model = available_models[i]
            for k in range(len(wordlist)):
                prompt = instructions + wordlist[k]
                #this object will be passed directly to curl_request as the message object
                message_object = '{{"model":"{}", "prompt":"{}", "stream":false}}'.format(model, prompt)
                key = model + "_" + wordlist[k] + "_" + str(n+1)
                keylist.append(key)
                promptlist.append(message_object)
    outlist = [keylist, promptlist]
    return outlist

#print(make_prompts(task_instructs, prompt_words, load_models("models.txt"), 2))

def parse_message(response_string):
    response_json = json.loads(response_string)
    #print(response_json)
    try:
        response_text = response_json["response"]
        return response_text
    except KeyError as e:
        print(e)

# model and prompt should be strings
# using subprocesses because post requests are annoying with this API and curl is better
def curl_request(message_object):
    #double brackets to escape the ones that matter so you dont get yelled at
    #payload = f'{{"model":"{model}", "prompt":"{prompt}", "stream":false}}'
    command = ["curl", URL,"-s", "-d", message_object]
    try:
        response = subprocess.run(command, stdout=subprocess.PIPE, universal_newlines=True, check=True)
        #print("Response:", response.stdout, type(response.stdout))
        return parse_message(response.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        return "ERROR IN API CALL: {}".format(e)

#n_per_config specifies the number of essays to generate per unique combo of model (ie specific params)
#and specific prompt in case we need more essays
def gen_essays(promptlist, outpath):
    keys = promptlist[0]
    prompts = promptlist[1]
    essays = {}
    for i in tqdm(range(len(keys)), desc="Doing your job for you", unit="Essays"):
        curr_prompt = prompts[i]
        curr_essay = curl_request(curr_prompt)
        essays[keys[i]] = curr_essay
    print(len(essays))
    with open(outpath, "w") as feil:
        json.dump(essays, feil)

test_p = [["marioyoyo", "llama33yoyo"],['{"model":"mario", "prompt":"yoyo", "stream":false}', '{"model":"llama3.3", "prompt":"yoyo", "stream":false}']]

# test = curl_request("mario", "Hey")
# print(test)

def main():
    parser = argparse.ArgumentParser(description="This script is used for generating short stories")
    parser.add_argument("-u", "--url", type=str, required=False, help=f"Specify url for ollama API, default is: 127.0.0.1:11438. Generally ollama runs on 11434 so if broken change this first")
    parser.add_argument("-mf", "--model-list", type=str, required=True, help=".txt file that contains the list of all models to be used. It should be a .txt file with model names saperated commas NO WHITESPACE EVER EVER EVER")
    parser.add_argument("-of", "--output-file", type=str, required=True, help=".json filepath where essays will be written to")
    parser.add_argument("-n", "--num-per-prompt", type=int, required=False, help="Use if you want to make more than 1 essay per prompt, default is 1")
    args=parser.parse_args()


    if args.url is not None:
        global URL
        URL = args.url

    if args.num_per_prompt is not None:
        global NUM_PER_PROMPT
        NUM_PER_PROMPT = args.num-per-prompt

    model_list = load_models(args.model_list)
    outputfile = args.output_file

    prompt_set = make_prompts(task_instructs, prompt_words, model_list)
    gen_essays(prompt_set, outputfile)

if __name__ == "__main__":
    main()


