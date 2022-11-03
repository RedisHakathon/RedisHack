# ArXiv Search Hackathon with Redis, SaturnCloud & Streamlit  
  
This is the code accompanying [this post](https://medium.com/@aaomar/arxiv-search-hackathon-with-redis-saturncloud-streamlit-d65ab0e0be2c). You can try the app [here](http://localhost:8501). Built using Streamlit and deployed on Heroku

**Note**: Redis Enterprise software is available on Amazon’s AWS Marketplace, Google Cloud Marketplace, and the Microsoft Azure Marketplace with the ease of single-click deployment. Simply choose the instance type for the nodes in your cluster and see how easy it is to handle millions of ops/sec while ensuring sub-millisecond latency. You can even test our failover mechanism by shutting down one of the nodes of your cluster, you’ll find that Redis Enterprise continues to work with zero effect on your traffic.  


![qa_streamlit](resources/qa_streamlit.gif)


## Libraries Used
* `Redis`
* `Transformers`
* `Streamlit`  

## Running Locally
All the experimentation were done on `Saturn Cloud`.

1. Download arXiv Dataset. Pull the arXiv dataset from the the following [Kaggle link](https://www.kaggle.com/datasets/Cornell-University/arxiv). Download and extract the zip file and place the resulting json file (arxiv-metadata-oai-snapshot.json) in the data/ directory.
