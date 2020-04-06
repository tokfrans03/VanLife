# Vanlife

a vue and python backend for a perfect vanlife experience


# Backend

Med denne kan du skicka notifikationer och ändra lampor via rf

## GET

Ger dig config.json med lamp koder + lösenord etc

för att refresha configen:

/refresh

## POST

skicka en notifikation:

    {
    	"action": "notif",
    	"value": {
    		"title": "Hej",
    		"message": "HALLå"
    	}
    }

skicka en RF kod 


    {
    	"action": "rf",
    	"value": 4353281 # Av/På
    }
