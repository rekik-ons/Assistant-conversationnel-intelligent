import axios from "axios";

const API_URL = "http://127.0.0.1:8000";


export const sendMessage = async (sessionId, message) => {

    const response = await axios.post(
        `${API_URL}/conversation/message/${encodeURIComponent(sessionId)}`,
        {
            message: message
        }
    );

    return response.data;
};


export const getConversation = async (sessionId) => {

    const response = await axios.get(
        `${API_URL}/conversation/${encodeURIComponent(sessionId)}`
    );

    return response.data;
};


export const getMessages = async (sessionId) => {

    const response = await axios.get(
        `${API_URL}/conversation/${encodeURIComponent(sessionId)}/messages`
    );

    return response.data;
};