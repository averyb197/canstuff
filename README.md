# canstuff

Code used to generate a lot of short stories. I am doing this to give one to every child in america so that they may cheat.

This code includes everything necessary to set up the models, and then generate an essay set with different parameters.

## **Creating Models In Ollama:**

### **Generate Modelfiles:**

Write model files with desired parameters and then save the file with no file extension 

Example Modelfile:

```plaintext 
FROM llama3.3:latest

PARAMETER temperature 0.7
```
### **Move The Model Files To Where Ollama Can Find It**

Make a directory for the modelfiles in the docker container:

```
docker exec -it ollama bash
```
Then:
```
mkdir MODELFILEDIRECTORY
```
Then exit bash and move the file with:
```
docker cp FILENAME ollama:/MODELFILE DIRECTORY/FILENAME
```

### **Build Models**

Go back into bash in the container then run:
```
ollama create MODELNAME –f FILENAME
```

Now you can generate the whole set of essays with ```genrate_essays.sh``` or generate individual sets with ``main.py``

## **Generating Essays**
Example for generate an individual set with ```main.py```

```bash
python3 main.py --url 127.0.0.1:11434 --model-list 
```


