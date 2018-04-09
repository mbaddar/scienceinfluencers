# **Science Infuencers:**

### An ArXiv paper search tool

* Using [Arxiv](https://arxiv.org/) API to search for papers
* Using [Semantic Scholar](https://www.semanticscholar.org/) to get influence details. Not all papers have matching records there.


### Content:
<a href="#1">1. Running the app:</a> <br>
<a id="2">2. Containerization:</a>
<a id="3">3. Implementation</a>
<a id="4">4. Hurdles:</a>
<a id="5">5. Future work:</a>

### [1. Running the app:](#1)
* Container endpoint: 

### [2. Containerization:](#2)

* Docker image built on the AWS staging machine
* Using [docker cloud](https://cloud.docker.com/) to proxy container hosting on AWS
* Image pushed to [Docker hub](https://hub.docker.com/r/baddar/scienceinfluencers/) repository: https://hub.docker.com/r/baddar/scienceinfluencers/
* Docker cloud linked with github for continuous intergration. Unfortunately building on docker hub is very unstable. However I have tried to push updates and it automatically triggers a new image build and deply. This also can be controlled by tagging the image and branching on github (To build a staging container for instance)
* Discarded docker cloud build and used an AWS instance to build the image then push it to docker hub 
* Used google clould shell (Tutorial [here](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app)) to build the image and push it to GCP then create a Kubernetes cluster. Still in progress

### [3. Implementation:](#3):

* Arxiv [API](https://arxiv.org/help/api/index): Outputs XML. I parsed it into a pandas dataframe and convert it to HTML, then manually inject hrefs for the URLs as pandas cannot do that
* Using JQuery and DataTables to add sort and pagination to the results
* No database implementation
* Google authentication implemented for login. However user data is not stored 

### [4. Hurdles:](#4):
* Using Docker Cloud to build my docker image. 
* Using Alpine Linux image at first. Since Pandas and many of its dependencies has to be built from source. 

### [5. Future work:](#5)

 * Adding Timeline: Histogram trends over time 
 * Include twitter influence analysis. Semantic scholar does this but no API was exposed
 * Database
 * Add more ArXiv [query](https://arxiv.org/find) capabilities: Search by title, author, etc

 