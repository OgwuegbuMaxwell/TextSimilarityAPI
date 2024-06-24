TextSimilarityAPI is a Flask-based RESTful API that allows users to calculate the textual similarity between two pieces of text. It leverages the spaCy NLP library to compute similarity scores using the en_core_web_md model.

### **Features**

- User Registration: Allows users to register to the API.
- Token Management: Users have tokens which are used as credits for accessing the API's resources.
- Text Similarity Detection: Users can submit two pieces of text and receive a similarity score.
- Token Refilling: Admins can refill tokens for any user account.


### **Installation**

Ensure you have Docker installed on your machine. Clone this repository, navigate to the project directory, and use Docker Compose to build and run the services.

```
git clone https://theRepo.git
cd TextSimilarityAPI
docker-compose up --build
```

### **Usage**
Register a New User

**POST /register**
{
  "username": "maxifreelancing",
  "password": "123456"
}


**Calculate Text Similarity**
Requires authentication (username and password).

```
{
    "username":"maxifreelancing",
    "password": "123456",
    "text1": "The developer committed the latest changes to the repository after the code review was completed.",
    "text2": "The programmer saved new updates to the project after checking the code."
}
```

**Refill Tokens**
Only accessible by admin accounts.



**POST /refill**
**{
  "username": "admin",
  "admin_password": "adminpass",
  "user": "maxifreelancing",
  "refill": 10
}**


### **API Endpoints**

- /register - Register a new user.
- /detect - Submit texts for similarity scoring.
- /refill - Refill tokens for a user account.
- /token - Check the number of tokens remaining.



### **Technologies**

- Flask: Python web framework.
- MongoDB: NoSQL database.
- Docker: Containerization platform.
- spaCy: Natural Language Processing library.


Ogwuegbu Maxwell - Initial work - [GitHub Profile](https://github.com/OgwuegbuMaxwell)


### **Acknowledgments**

- Thanks to the spaCy team for providing an excellent NLP library.
- Flask community for a great micro-framework for APIs.


### **Results and Findings**

**Overview**
Our TextSimilarityAPI leverages the **en_core_web_md** model from spaCy to compute similarity scores between pairs of texts. This model incorporates medium-sized word vectors which capture semantic meanings of words to some extent, but it may still have limitations in certain contexts.


### **Performance Highlights**

1. Similar Phrasing and Synonyms: The model effectively identifies similarity in sentences with similar structures or synonyms. For example:

- Text 1: "The quick brown fox jumps over the lazy dog."
- Text 2: "A fast brown fox leaps over a lazy dog."
- Similarity: 79.63%
This result demonstrates the model's capability to recognize synonymous terms and similar sentence structures.


2. Contextual Differences:

- Text 1: "Apple launched a new product that will revolutionize the market."
- Text 2: "I ate a delicious apple for lunch today."
- Similarity: 58.63%

Despite the contextual differences between a tech company's product launch and eating a fruit, the presence of the homonym "apple" in both sentences leads to a moderate similarity score. This indicates that while the model recognizes lexical similarities, it may struggle with context disambiguation.


### **Implications for Usage**
The API is well-suited for applications where the primary requirement is to gauge text similarity based on vocabulary and basic semantic structures. However, for use cases involving nuanced understanding of context, especially where homonyms or highly context-dependent meanings are involved, the results may not always align perfectly with human judgment.




![img1](https://github.com/OgwuegbuMaxwell/TextSimilarityAPI/assets/53094485/f24a95b7-b19d-468a-94db-f21b96bba331)

![img2](https://github.com/OgwuegbuMaxwell/TextSimilarityAPI/assets/53094485/159d297c-5196-46d9-bee8-cda816e0882d)

![img3](https://github.com/OgwuegbuMaxwell/TextSimilarityAPI/assets/53094485/4db27eeb-6e07-48b6-9854-81e40b768561)


This behavior underscores the importance of selecting the right NLP model and configuration for specific applications, considering the strengths and weaknesses of the model being used.

### **Recommendations**
Fine-Tuning: For applications requiring high contextual sensitivity, consider fine-tuning the model on domain-specific texts or employing more advanced models designed for greater context awareness.
Model Upgrade: Consider experimenting with transformer-based models like **en_core_web_trf** for potentially better handling of complex semantic relationships due to their deeper contextual analysis capabilities.
