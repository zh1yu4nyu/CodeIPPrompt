# CodeIPPrompt

CodeIPPrompt is developed to assess the extent to which code language models can plagiarize licensed code in its learnt programs. Details regarding this work can be found in the [paper](https://icml.cc/virtual/2023/poster/24354) and project website at [https://sites.google.com/view/codeipprompt](https://sites.google.com/view/codeipprompt). Its key functionalities are enabled by prompt construction from source dode, and similarity measurement based on [JPlag](https://github.com/jplag/JPlag) and [Dolos](https://github.com/dodona-edu/dolos). 

# Abstract
Recent advances in large language models (LMs) have facilitated their ability to synthesize programming code. However, they have also raised concerns about intellectual property (IP) rights violations. Despite the significance of this issue, it has been relatively less explored. In this paper, we aim to bridge the gap by presenting CodeIPPrompt, a platform for automatic evaluation of the extent to which code language models may reproduce licensed programs. It comprises two key components: prompts constructed from a licensed code database to elicit LMs to generate IP-violating code, and a measurement tool to evaluate the extent of IP violation of code LMs. We conducted an extensive evaluation of existing open-source code LMs and commercial products and revealed the prevalence of IP violations in all these models. We further identified that the root cause is the substantial proportion of training corpus subject to restrictive licenses, resulting from both intentional inclusion and inconsistent license practice in the real world. To address this issue, we also explored potential mitigation strategies, including fine-tuning and dynamic token filtering. Our study provides a testbed for evaluating the IP violation issues of the existing code generation platforms and stresses the need for a better mitigation strategy. 

# Installation

The Python packages required to run the programs are numpy (tested on 1.21.2) and pyarrow (tested on 10.0.1). The binary of JPlag can be downloaded from the official [JPlag release](https://github.com/jplag/jplag/releases). For the Java component, please install [Dolos library](https://www.npmjs.com/package/@dodona/dolos-lib) following official instructions. 

Since it requires the JavaScript runtime Node.js with version 14 or higher, please first check your version with the command
```sh
$ node --version
```
If it reports an error or a version older than 14, please install Node following the official [instructions](https://dolos.ugent.be/guide/installation.html#install-node-js). The platform has been tested with openjdk version 17.0.6, nodejs version v16.19.1, and npm version 8.19.3. 

Then please install dolos with
```sh
$ npm install -g @dodona/dolos
```
Up to the date of release, this will install the latest version of dolos at v2.1.0. You can check the version by 
```sh
$ dolos --version
```
And a sample output looks like this: 
```sh
Dolos v2.1.0
Node v16.19.1
Tree-sitter v0.20.1
```

Please note that the default dolos does not come with cpp parser, so please add the parser following the official [instructions](https://dolos.ugent.be/guide/languages.html#adding-a-new-language). In our setup, you can add it by:
```sh
$ npm install -g tree-sitter-cpp@0.20
```

At last, the environment settings for code generation can vary for different models (e.g., CodeGen, CodeParrot), which are therefore not detailed here. 

# Usage

CodeIPPrompt is a evaluation platform consisting of two major components, prompt construction and code generation model evaluation.

## Prompt Construction

The prompt construction procedure is designed to be generalized to any given (licensed) source code database with programming language of Python, C, C++, C#, and Java. The script prompt_github.py constructs prompts from a given folder containing GitHub repositories. To use it, you need to specify the license and programming language of the target prompts, such as:
```sh
$ python3 prompt_github.py agpl3 python
```

Several sets of prompts derived from real-world licensed code from GitHub can be downloaded at [https://zenodo.org/record/7987148](https://zenodo.org/record/7987148).

## Model Evaluation

To evaluate a given code generation model, please run the model on the constructed prompts. An example of generating programs using CodeParrot is provided in Example_Parrot.py, please replace the paths in your setup. An example is:
```sh
$ python3 Example_Parrot codeparrot/codeparrot prompts_agpl3_python_2023-03-27-21-21-29
```

Once programs have been generated and saved in the *Programs* directory, run model_eval.py to obtain the results and save them in CSV files. For example:
```sh
$ python3 model_eval.py codegen2Bmulti_agpl3_python_2023-03-27-20-32-30
```

At last, please use results.py to get the final results in terms of *Expected Maximum (EM)* and *Empirical Probability (EP)*. For example:
```sh
$ python3 results.py codegen2Bmulti 
```

# Citation

If you find the platform useful, please cite our work with the following reference:
```
@inproceedings{yu2023codeipprompt,
  title={CodeIPPrompt: Intellectual Property Infringement Assessment of Code Language Models},
  author={Yu, Zhiyuan and Wu, Yuhao and Zhang, Ning and Wang, Chenguang and Vorobeychik, Yevgeniy and Xiao, Chaowei},
  booktitle={International conference on machine learning},
  year={2023},
  organization={PMLR}
}
```
