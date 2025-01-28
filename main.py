import subprocess
import json
import argparse
from tqdm import tqdm

#url for where to reach the ollama API
URL = "127.0.0.1:11438/api/generate"

# basically a .csv but round here we call it a .txt
def load_models(models_path):
    with open(models_path, "r") as feil:
        rawtxt = feil.read()
        models = rawtxt.split(",")
        models = [mod.strip("\n") for mod in models]
        return models

#generate the prompts for the models 
def make_prompts(instructions, wordlist, available_models, grade_level, LENGTH, NUM_PER_PROMPT):
    promptlist = []
    keylist = []
    for n in range(NUM_PER_PROMPT):
        for i in range(len(available_models)):
            model = available_models[i]
            for k in range(len(wordlist)):
                prompt = instructions + wordlist[k] + " Only include the story in your response"
                #this object will be passed directly to curl_request as the message object
		#DO NOT YELL AT ME FOR USING .format() I WAS ORIGINALLY TRYING TO GET THIS TO RUN ON PYTHON 2
		#UNTIL I DISCOVERED HOW TO TYPE python3 
                message_object = '{{"model":"{}", "prompt":"{}", "stream":false}}'.format(model, prompt)
                key = model + "_" + wordlist[k] + "_" + str(n+1) +"_" + grade_level + "_" +  LENGTH
                keylist.append(key)
                promptlist.append(message_object)
    outlist = [keylist, promptlist]
    return outlist

#Extract text from the response
def parse_message(response_string):
    response_json = json.loads(response_string)
    try:
        response_text = response_json["response"]
        return response_text
    except KeyError as e:
        print(e)

# model and prompt should be strings
# using subprocesses because post requests are annoying with this API and curl is better
def curl_request(message_object):
    command = ["curl", URL,"-s", "-d", message_object]
    try:
        response = subprocess.run(command, stdout=subprocess.PIPE, universal_newlines=True, check=True)
        return parse_message(response.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        return "ERROR IN API CALL: {}".format(e)

#n_per_config specifies the number of essays to generate per unique combo of model (ie specific params)
#and specific prompt 

def gen_essays(promptlist, outpath):
    keys = promptlist[0]
    prompts = promptlist[1]
    essays = {}
    for i in tqdm(range(len(keys)), desc="Doing your job for you", unit="Essay"):
        curr_prompt = prompts[i]
        curr_essay = curl_request(curr_prompt)
        essays[keys[i]] = curr_essay
    print(len(essays))
    with open(outpath, "w") as feil:
        json.dump(essays, feil, indent=4)



def main():
    parser = argparse.ArgumentParser(description="This script is used for generating short stories")
    parser.add_argument("-u", "--url", type=str, required=False, help=f"Specify url for ollama API, default is: 127.0.0.1:11438. Generally ollama runs on 11434 so if broken change this first")
    parser.add_argument("-mf", "--model-list", type=str, required=True, help=".txt file that contains the list of all models to be used. It should be a .txt file with model names saperated commas NO WHITESPACE EVER EVER EVER")
    parser.add_argument("-of", "--output-file", type=str, required=True, help=".json filepath where essays will be written to")
    parser.add_argument("-n", "--num-per-prompt", type=int, required=False, help="Use if you want to make more than 1 essay per prompt, default is 1")
    parser.add_argument("-g", "--grade-level", type=str, required=False, help="Used to specify the grade level of the essays to be generated. Default is no specification. Specification uses slightly different prompt. May be a numerical value eg 8 or string eg. Undergraduate. See docs for details")
    parser.add_argument("-l", "--length", type=str, required=False, help="Specify Length of the essays. Default is short (4-6 sentences). Long = 7-8 sentences.")
    args=parser.parse_args()

    LENGTH = "short"
    length_string = "4-6"
#    URL = "127.0.0.1:11438/api/generate"

    NUM_PER_PROMPT = 1
    GRADE_LEVEL = None


    if args.url is not None:
        global URL
        URL = args.url

    if args.num_per_prompt is not None:
        NUM_PER_PROMPT = args.num_per_prompt

    if args.length == "long":
        length_string = "7-8"
        LENGTH = "long"
    if args.length is None:
        print("No Length Specified, defaulting to short (4-6)")

    if args.grade_level is not None:
        GRADE_LEVEL = args.grade_level

    task_instructs = (f"You will be given 3 words, and you must write a very short story "
                      f"that is {length_string}  sentences long, that includes all 3 words. Try to use your imagination and be creative "
                      f"when writing your story. The 3 words are: ")

    varied_grade_instructs = (
        f"You will be given 3 words, and you must write a very short story at a grade {GRADE_LEVEL} reading level "
        f"that is {length_string} sentences long, that includes all 3 words. Try to use your imagination and be creative "
        f"when writing your story. The 3 words are: ")

    prompt_words = [
        "stamp-letter-send",
        "petrol-diesel-pump",
        "year-week-embark",
        "statement-stealth-detect",
        "belief-faith-sing",
        "organ-empire-comply",
        "gloom-payment-exist"
    ]

    model_list = load_models(args.model_list)
    outputfile = args.output_file

    if args.grade_level is not None:
        prompt_set = make_prompts(varied_grade_instructs, prompt_words, model_list,GRADE_LEVEL, LENGTH, NUM_PER_PROMPT)
    else:
        prompt_set = make_prompts(task_instructs, prompt_words, model_list,"unspecGrade", LENGTH, NUM_PER_PROMPT)
   
    gen_essays(prompt_set, outputfile)

if __name__ == "__main__":
    main()


