<html>
    <p align="center"> 
        <img src="https://github.com/RedisHakathon/arXiv-search-hackathon-with-redis-saturnCloud/blob/main/resource/mlops.community%20logo.jpg" alt="Mlops Logo" width="100">
    </p>
    <h1 align="center">
        Mlops Engineering Lab
    </h1>
    <p align="center">
        Open Source Repository for MLops Engineering Lab Hackathon
    </p>
    <p align="center">
        <a href="https://go.mlops.community/slack">
            <img src="https://img.shields.io/badge/slack-join_chat.svg?logo=slack&style=social" alt="Slack" />
        </a>
    </p>
</html> 
  
This is the code accompanying [this post](https://medium.com/@aaomar/arxiv-search-hackathon-with-redis-saturncloud-streamlit-d65ab0e0be2c). You can try the app [here](https://redishakathon-arxiv-search-hackathon-with-redis-satu-app-txqqb0.streamlit.app/). Built using Streamlit and deployed on Streamlit Cloud

**Note**: Streamlit app is deployed with two pre-trained models, which is quite huge thus the use of streamlit caching to enhance performance. However, there's a slug with the appilication on the first spin. We thank Redis & Saturn Cloud folks who helped us with not only resources but also 24/7 Support.  
  
    
    
  
![App](https://github.com/RedisHakathon/arXiv-search-hackathon-with-redis-saturnCloud/blob/main/resource/StreamlitApp.gif)



## Libraries Used
* `Redis`
* `Transformers`
* `Streamlit`  

## Running Experimentation
All the experimentation were done on `Saturn Cloud`.

1. Run end-to-end experimentation on jupyter notebook [Saturn Cloud](https://github.com/RedisHakathon/arXiv-search-hackathon-with-redis-saturnCloud/blob/main/backend/SaturnCloud-T4-XLarge%20Jupyter.ipynb)    

| **📝 Note** |
|:---------|
| You Can get 30 hours a month free of 64GB RAM and GPU instances, see [here](https://saturncloud.io/). |  

Then import `redis_url`:

<details>

<summary>💻 REDIS_URL</summary>

---

```bash
 import os
     INDEX_NAME = "index"
     REDIS_HOST = os.environ.get("REDIS_HOST", "--host--name")
     REDIS_PORT = os.environ.get("REDIS_PORT", --port--number)
     REDIS_DB = os.environ.get("REDIS_DB", "--database_name--")
     REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD","--password--")
     REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
```

---

</details>  

<details>

<summary>ℹ Interacting with Redis Enterprise</summary>

---

Check if there's index in the database:

```
FT._LIST
```

Check for Index data:

```
FT.INFO <index_name>
```

---

</details>

| **📝 Note** |
|:---------|
| You Can get a free Redis Enterprise, see the [Try for free](https://redis.com/try-free/). |  


## 💻 Streamlit App 

The `project` ships with a `app.py` script that uses
[`streamlit`](https://streamlit.io/) as a UI for interacting with your redis database.  

```bash
git clone https://github.com/RedisHakathon/arXiv-search-hackathon-with-redis-saturnCloud
```  
  
  ### install requirements    
``` 
pip install -r requirements.txt 
```  

<details>

<summary> Run streamlit locally </summary>

---

```bash
streamlit run app.py
```

---

</details>    

