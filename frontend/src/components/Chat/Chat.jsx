import { useEffect, useRef, useState } from "react";

import {
    sendMessage,
    getConversation,
    getMessages
} from "../../services/conversationService";

import "./Chat.css";


function Chat() {

    // ==========================================================
    // ÉTATS
    // ==========================================================

    const [sessionId, setSessionId] = useState("");
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [terminee, setTerminee] = useState(false);
    const [result, setResult] = useState(null);

    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);


    // ==========================================================
    // INITIALISATION
    // ==========================================================

    useEffect(() => {

        let session = localStorage.getItem("taysir_session_id");

        if (!session) {
            session = crypto.randomUUID();
            localStorage.setItem("taysir_session_id", session);
        }

        setSessionId(session);
        chargerConversation(session);

    }, []);


    // ==========================================================
    // DÉFILEMENT AUTOMATIQUE VERS LE BAS
    // ==========================================================

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({
            behavior: "smooth",
            block: "end"
        });
    }, [messages, loading, result]);


    // ==========================================================
    // FOCUS AUTOMATIQUE SUR LE CHAMP DE SAISIE
    // ==========================================================

    useEffect(() => {
        if (!loading && !terminee) {
            inputRef.current?.focus();
        }
    }, [loading, terminee, sessionId]);


    // ==========================================================
    // OUTIL : TRANSFERT AU CONSEILLER
    // ==========================================================

    const calculerTransfert = (data) =>
        data.eligibilite === "Éligible" &&
        (
            data.qualification === "Prospect chaud" ||
            data.qualification === "Prospect tiède"
        );


    // ==========================================================
    // CHARGER L'HISTORIQUE
    // ==========================================================

    const chargerConversation = async (session) => {

        try {

            const conversation = await getConversation(session);
            const historique = await getMessages(session);

            setMessages(
                historique.map((msg) => ({
                    role: msg.role,
                    contenu: msg.contenu
                }))
            );

            if (conversation.etape === "fin") {

                setTerminee(true);

                if (conversation.data) {
                    setResult({
                        ...conversation.data,
                        transfert_conseiller: calculerTransfert(
                            conversation.data
                        )
                    });
                }
            }

        } catch (error) {
            console.log("Nouvelle conversation");
        }

    };


    // ==========================================================
    // ENVOYER MESSAGE
    // ==========================================================

    const handleSend = async (event) => {

        event.preventDefault();

        if (!message.trim() || loading || terminee) {
            return;
        }

        const texteUtilisateur = message.trim();

        setMessage("");
        setLoading(true);

        setMessages((previous) => [
            ...previous,
            { role: "user", contenu: texteUtilisateur }
        ]);

        try {

            const response = await sendMessage(
                sessionId,
                texteUtilisateur
            );

            // Réponse finale (objet)
            if (typeof response.response === "object") {

                const resultData = response.response.data;

                setResult({
                    ...resultData,
                    transfert_conseiller: calculerTransfert(resultData)
                });

                setMessages((prev) => [
                    ...prev,
                    {
                        role: "assistant",
                        contenu: response.response.message
                    }
                ]);

            }
            // Réponse normale (texte)
            else {

                setMessages((prev) => [
                    ...prev,
                    {
                        role: "assistant",
                        contenu: response.response
                    }
                ]);

            }

            if (response.etape === "fin") {
                setTerminee(true);
            }

        } catch (error) {

            console.error("Erreur API :", error);

            setMessages((previous) => [
                ...previous,
                {
                    role: "assistant",
                    contenu:
                        "Une erreur est survenue lors de la communication avec le serveur."
                }
            ]);

        } finally {

            setLoading(false);

        }

    };


    // ==========================================================
    // NOUVELLE CONVERSATION
    // ==========================================================

    const nouvelleConversation = () => {

        const nouvelleSession = crypto.randomUUID();

        localStorage.setItem("taysir_session_id", nouvelleSession);

        setSessionId(nouvelleSession);
        setMessages([]);
        setMessage("");
        setTerminee(false);
        setResult(null);

    };


    // ==========================================================
    // INTERFACE
    // ==========================================================

    return (

        <div className="chat-page">

            <div className="chat-container">

                {/* HEADER */}

                <div className="chat-header">

                    <div>
                        <h1>Taysir Microfinance</h1>
                        <p>Assistant de qualification</p>
                    </div>

                    {terminee && (
                        <button
                            className="new-chat-button"
                            onClick={nouvelleConversation}
                        >
                            Nouvelle conversation
                        </button>
                    )}

                </div>


                {/* ZONE SCROLLABLE : MESSAGES + RÉSULTAT */}

                <div className="chat-scroll-area">

                    <div className="chat-messages">

                        {/* bienvenue */}

                        {messages.length === 0 && (
                            <div className="welcome-message">
                                <h2>Bienvenue</h2>
                                <p>
                                    Je vais vous accompagner dans votre
                                    demande de financement.
                                </p>
                            </div>
                        )}

                        {/* historique */}

                        {messages.map((msg, index) => (
                            <div
                                key={index}
                                className={
                                    msg.role === "user"
                                        ? "message user-message"
                                        : "message assistant-message"
                                }
                            >
                                <div className="message-content">
                                    {msg.contenu}
                                </div>
                            </div>
                        ))}

                        {/* loading */}

                        {loading && (
                            <div className="message assistant-message">
                                <div className="message-content typing">
                                    Taysir est en train de répondre...
                                </div>
                            </div>
                        )}

                    </div>


                    {/* résultat du prospect */}

                    {result && (

                        <div className="prospect-result">

                            <h2>Résultat de votre demande</h2>

                            <div className="score-result">
                                <span>Votre score</span>
                                <strong>{result.score} / 100</strong>
                            </div>

                            {result.transfert_conseiller ? (

                                <div className="transfer-message success">
                                    <h3>Votre profil est favorable</h3>
                                    <p>
                                        Votre demande va être transmise à un
                                        conseiller Taysir pour la suite du
                                        traitement.
                                    </p>
                                </div>

                            ) : (

                                <div className="transfer-message refused">
                                    <h3>Demande non transmise</h3>
                                    <p>
                                        Votre profil ne répond pas
                                        actuellement aux critères permettant
                                        une transmission au conseiller.
                                    </p>
                                </div>

                            )}

                        </div>

                    )}

                    {/* repère de fin pour le défilement automatique */}
                    <div ref={messagesEndRef} />

                </div>


                {/* SAISIE */}

                <form
                    className="chat-input-container"
                    onSubmit={handleSend}
                >

                    <input
                        ref={inputRef}
                        autoFocus
                        autoComplete="off"
                        type="text"
                        value={message}
                        onChange={(event) =>
                            setMessage(event.target.value)
                        }
                        placeholder={
                            terminee
                                ? "Conversation terminée"
                                : "Écrivez votre message..."
                        }
                        disabled={loading || terminee}
                    />

                    <button
                        type="submit"
                        disabled={loading || terminee || !message.trim()}
                    >
                        Envoyer
                    </button>

                </form>

            </div>

        </div>

    );
}


export default Chat;