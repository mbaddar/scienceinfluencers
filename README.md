# Science Infuencers: 

An ArXiv paper search tool.

* Arxiv API to search for papers
* Semantic Scholar to get influence and citation velocity
* Research gate does not have an API unfortunately


### Running the app:
* Developed in a windows box 
* Staged on a [Linux AWS machine](http://ec2-34-236-12-185.compute-1.amazonaws.com:5000)
* Docker image built on the AWS staging machine
* Docker container pushed to dockerhub and deployed via docker cloud (on AWS)
* Kubernetes cluster creation in progress
* You can find the repository in [Docker hub](https://hub.docker.com/r/baddar/scienceinfluencers/)


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

 