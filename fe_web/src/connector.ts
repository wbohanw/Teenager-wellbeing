const API_URL = "http://127.0.0.1:5000"; 

interface ChatPreferences {
  language?: string;
  purpose?: string;
  personalityTraits?: string[];
  tone?: string;
  titlePreference?: string;
  properNouns?: string[];
  [key: string]: any;
}

interface ChatResponse {
  response: string;
  [key: string]: any;
}

export const sendMessageToChatbot = async (message: string, preferences: ChatPreferences = {}): Promise<ChatResponse> => {
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message,
                preferences
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Server error details:", errorData);
            throw new Error(`HTTP error! Status: ${response.status}. Details: ${errorData.error || 'Unknown error'}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Error sending message to chatbot:", error);
        return { response: "Sorry, there was an error communicating with the chatbot." };
    }
}

export const savePreferencesToBackend = async (preferences: ChatPreferences): Promise<{status: string, message: string}> => {
    try {
        const response = await fetch('http://localhost:5000/preferences', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(preferences),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        return await response.json();
    } catch (error) {
        console.error('Error saving preferences to backend:', error);
        return { status: 'error', message: "Failed to save preferences" };
    }
}; 