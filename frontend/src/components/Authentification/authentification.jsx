import { useState } from "react";
import { useNavigate } from "react-router-dom";

import "./Authentification.css";

export default function Authentification() {
    const navigate = useNavigate();

    const [login, setLogin] = useState("");
    const [mdp, setMdp] = useState("");
    const [message, setMessage] = useState(null); // { type, texte }
    const [loading, setLoading] = useState(false);

    const afficherMessage = (type, texte, duree = 3000) => {
        setMessage({ type, texte });
        setTimeout(() => setMessage(null), duree);
    };

    const submit = async (e) => {
        e.preventDefault();
        setMessage(null);
        setLoading(true);

        try {
            const res = await fetch("http://localhost:8000/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    login: login.trim(),
                    mot_de_passe: mdp,
                }),
            });

            if (!res.ok) {
                afficherMessage("error", "Connexion échouée : login ou mot de passe incorrect.");
                return;
            }

            const user = await res.json();
            localStorage.setItem("user", JSON.stringify(user));

            afficherMessage("success", "Connexion effectuée", 1200);

            // On laisse l'alerte visible un instant avant de rediriger
            setTimeout(() => {
                navigate(
                    user.role === "administrateur" ? "/admin" : "/conseiller",
                    { replace: true }
                );
            }, 1200);

        } catch {
            afficherMessage("error", "Connexion échouée : serveur inaccessible.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-page">

            {/* Conteneur : l'alerte est positionnée par rapport à lui, juste au-dessus de la carte */}
            <div
                style={{
                    position: "relative",
                    width: "100%",
                    maxWidth: "520px",
                }}
            >

                {message && (
                    <div
                        style={{
                            position: "absolute",
                            bottom: "100%",
                            left: 0,
                            right: 0,
                            marginBottom: "16px",
                            boxSizing: "border-box",
                            padding: "16px 28px",
                            borderRadius: "10px",
                            fontSize: "15px",
                            fontWeight: 600,
                            textAlign: "center",
                            boxShadow: "0 4px 14px rgba(0,0,0,0.15)",
                            background: message.type === "success" ? "#dcfce7" : "#fee2e2",
                            color: message.type === "success" ? "#166534" : "#b91c1c",
                            
                        }}
                    >
                        {message.texte}
                    </div>
                )}

                <form
                    className="auth-card"
                    onSubmit={submit}
                    style={{
                        width: "100%",
                        maxWidth: "520px",
                        padding: "50px 45px",
                        gap: "26px",
                    }}
                >

                    <div className="auth-header">
                        <h1 style={{ color: "#123c69", fontSize: "32px" }}>
                            Taysir Microfinance
                        </h1>
                        <p style={{ fontSize: "16px" }}>
                            Connectez-vous à votre espace
                        </p>
                    </div>

                    <div className="auth-field">
                        <label htmlFor="login" style={{ fontSize: "15px" }}>
                            Login
                        </label>
                        <input
                            id="login"
                            type="text"
                            placeholder="Tapez votre login"
                            value={login}
                            onChange={(e) => setLogin(e.target.value)}
                            autoFocus
                            required
                            style={{ padding: "15px 16px", fontSize: "16px" }}
                        />
                    </div>

                    <div className="auth-field">
                        <label htmlFor="mdp" style={{ fontSize: "15px" }}>
                            Mot de passe
                        </label>
                        <input
                            id="mdp"
                            type="password"
                            placeholder="Tapez votre mot de passe"
                            value={mdp}
                            onChange={(e) => setMdp(e.target.value)}
                            required
                            style={{ padding: "15px 16px", fontSize: "16px" }}
                        />
                    </div>

                    <button
                        className="auth-button"
                        type="submit"
                        disabled={loading}
                        style={{
                            background: "#3859b6",
                            color: "white",
                            border: "none",
                            borderRadius: "8px",
                            padding: "16px 18px",
                            fontSize: "16px",
                            fontWeight: 600,
                            cursor: loading ? "not-allowed" : "pointer",
                            opacity: loading ? 0.7 : 1,
                        }}
                    >
                        {loading ? "Connexion..." : "Se connecter"}
                    </button>

                </form>

            </div>
        </div>
    );
}