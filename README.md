# ** Science Infuencers: **

### Running the app:
* Container endpoint: 


### An ArXiv paper search tool:

* Using [Arxiv](https://arxiv.org/){:target="_blank"} API to search for papers
* Using [Semantic Scholar](https://www.semanticscholar.org/) to get influence details. Not all papers have matching records there.

### Containerization:

* Docker image built on the AWS staging machine
* Using [docker cloud](https://cloud.docker.com/) to proxy container hosting on AWS
* Image pushed to [Docker hub](https://hub.docker.com/r/baddar/scienceinfluencers/) repository: https://hub.docker.com/r/baddar/scienceinfluencers/
* Docker cloud linked with github for continuous intergration. Unfortunately building on docker hub is very unstable. However I have tried to push updates and it automatically triggers a new image build and deply. This also can be controlled by tagging the image and branching on github (To build a staging container for instance)
* Discarded docker cloud build and used an AWS instance to build the image then push it to docker hub 
* Used google clould shell (Tutorial [here](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app)) to build the image and push it to GCP then create a Kubernetes cluster. Still in progress

### Implementation:

* Arxiv [API](https://arxiv.org/help/api/index): Outputs XML. I parsed it into a pandas dataframe and convert it to HTML, then manually inject hrefs for the URLs as pandas cannot do that
* Using JQuery and DataTables to add sort and pagination to the results
* No database implementation
* Google authentication implemented for login. However user data is not stored 




### Hurdles:
* Using Alpine image at first
* Docker cloud build tool. Extremely slow. NOT recommended 
* Implementing Google authentication

Future work:

 * Streaming
 * UX: Sorting and filtering
 * Timeline 
 * Twitter
 * L8N
 * DB
 * Pagination
 * Add more query capabilities: Search by title, author, etc

 