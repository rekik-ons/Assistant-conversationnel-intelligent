import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
    getConversation,
    getMessages
} from "../../services/conversationService";

import "./AdminConversation.css";


function AdminConversation() {

    const { sessionId } = useParams();
    const navigate = useNavigate();

    const [conversation, setConversation] = useState(null);
    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    // ==========================================================
    // CHARGER LA CONVERSATION
    // ==========================================================

    useEffect(() => {

        chargerConversation();

    }, [sessionId]);


    const chargerConversation = async () => {

        try {

            setLoading(true);
            setError("");


            const [conversationData, messagesData] =
    await Promise.all([
        getConversation(sessionId),
        getMessages(sessionId)
    ]);


            setConversation(
                conversationData
            );


            setMessages(
                messagesData || []
            );


        } catch (err) {

            console.error(
                "Erreur conversation :",
                err
            );


            if (err.response?.status === 404) {

                setError(
                    "Conversation introuvable."
                );

            } else {

                setError(
                    "Impossible de charger la conversation."
                );

            }

        } finally {

            setLoading(false);

        }

    };


    // ==========================================================
    // LOADING
    // ==========================================================

    if (loading) {

        return (

            <div className="admin-conversation-page">

                <div className="conversation-loading">

                    Chargement de la conversation...

                </div>

            </div>

        );

    }


    // ==========================================================
    // ERROR
    // ==========================================================

    if (error) {

        return (

            <div className="admin-conversation-page">

                <div className="conversation-error">

                    <h2>
                        Erreur
                    </h2>

                    <p>
                        {error}
                    </p>


                    <button
                        onClick={() =>
                            navigate("/admin")
                        }
                    >
                        ← Retour au dashboard
                    </button>

                </div>

            </div>

        );

    }

    const sessionAffichage =
    sessionId === "9b3b0361-9778-4057-b23b-c01dde51488a"
        ? "test-01"
        : sessionId;
    return (

        <div className="admin-conversation-page">


            {/* ==================================================
                HEADER
                ================================================== */}

            <header className="conversation-header">

                <div>

                    <h1>
                        Taysir Microfinance
                    </h1>

                    <p>
                        Historique de conversation
                    </p>

                </div>


                <button
                    className="back-button"
                    onClick={() =>
                        navigate("/admin")
                    }
                >
                     Retour
                </button>

            </header>


            {/* ==================================================
                INFORMATIONS CONVERSATION
                ================================================== */}

            

            <section className="conversation-info">

                <div>

                    <span>
                        État
                    </span>

                    <strong>
                        {conversation?.etape === "fin"
                            ? "Conversation terminée"
                            : conversation?.etape || "-"
                        }
                    </strong>

                </div>

                <div>

                    <span>
                        Nombre de messages
                    </span>

                    <strong>
                        {messages.length}
                    </strong>

                </div>

            </section>

            {/* ==================================================
                MESSAGES
                ================================================== */}

            <main className="conversation-container">

                <div className="messages-list">

                    {messages.length === 0 ? (

                        <div className="empty-conversation">

                            Aucun message dans cette conversation.

                        </div>

                    ) : (

                        messages.map(
                            (msg) => (

                            <div
                                key={msg.id}
                                className={
                                    msg.role === "user"
                                        ? "conversation-message user"
                                        : "conversation-message assistant"
                                }
                            >

                                <div className="message-author">

                                    {msg.role === "user"
                                        ? "Prospect"
                                        : "Assistant"
                                    }

                                </div>


                                <div className="message-bubble">

                                    {msg.contenu}

                                </div>


                                <div className="message-date">

                                    {msg.date_creation
                                        ? new Date(
                                            msg.date_creation
                                        ).toLocaleString("fr-FR")
                                        : ""
                                    }

                                </div>

                            </div>

                        ))

                    )}

                </div>

            </main>

        </div>
    );
}


export default AdminConversation;