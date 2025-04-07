const API_URL = "http://127.0.0.1:5000"; 

export async function sendMessageToChatbot(message, userId = "default_user") {
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message, user_id: userId }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Server error details:", errorData);
            throw new Error(`HTTP error! Status: ${response.status}. Details: ${errorData.error || 'Unknown error'}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error connecting to chatbot API:", error);
        return { 
            error: "Failed to connect to chatbot.",
            details: error.message
        };
    }
}
