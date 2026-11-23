import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    getQualification,
    getNonQualifies,
    getProspectsParStatut
} from "../../services/dashboardService";

import "./ConseillerDashboard.css";


function ConseillerDashboard() {

    const navigate = useNavigate();

    const [prospects, setProspects] = useState([]);

    const [filtre, setFiltre] = useState("chaud");

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");

const [statutFiltre, setStatutFiltre] = useState("tous");


useEffect(() => {
    chargerProspects();
}, [filtre, statutFiltre]);


    const chargerProspects = async () => {

    try {

        setLoading(true);
        setError("");

        let data;


        // ==========================================
        // FILTRE PAR STATUT
        // ==========================================

        if (statutFiltre !== "tous") {

            data = await getProspectsParStatut(
                statutFiltre
            );

            setProspects(
                data.prospects || []
            );

            return;
        }


        // ==========================================
        // NON QUALIFIÉS
        // ==========================================

        if (filtre === "non_qualifie") {

            data = await getNonQualifies();

            setProspects(
                data.prospects || []
            );

            return;
        }


        // ==========================================
        // QUALIFICATION
        // ==========================================

        data = await getQualification(filtre);

        setProspects(
            data.prospects || []
        );


    } catch (err) {

        console.error(err);

        setError(
            err.response?.data?.detail ||
            "Impossible de charger les prospects."
        );

    } finally {

        setLoading(false);

    }
};


    const consulterProspect = (prospect) => {

        navigate(
            "/conseiller/prospect",
            {
                state: {
                    prospect: prospect
                }
            }
        );

    };


    return (

        <div className="conseiller-page">


            {/* ====================================== */}
            {/* HEADER */}
            {/* ====================================== */}

            <header
    className="conseiller-header"
    style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center"
    }}
>

    <div>
        <h1>Taysir Microfinance</h1>
        <p>Espace conseiller</p>
    </div>

    <button
        className="logout-button"
        onClick={() => {
            localStorage.removeItem("user");
            navigate("/authentification");
        }}
    >
        Se déconnecter
    </button>

</header>


            {/* ====================================== */}
            {/* FILTRES */}
            {/* ====================================== */}

            <section className="filters">


                <button
                    className={
                        filtre === "chaud"
                            ? "filter active chaud"
                            : "filter chaud"
                    }
                    onClick={() =>
                        setFiltre("chaud")
                    }
                >
                     Prospects chauds
                </button>


                <button
                    className={
                        filtre === "tiede"
                            ? "filter active tiede"
                            : "filter tiede"
                    }
                    onClick={() =>
                        setFiltre("tiede")
                    }
                >
                     Prospects tièdes
                </button>


                <button
                    className={
                        filtre === "froid"
                            ? "filter active froid"
                            : "filter froid"
                    }
                    onClick={() =>
                        setFiltre("froid")
                    }
                >
                     Prospects froids
                </button>


                <button
                    className={
                        filtre === "non_qualifie"
                            ? "filter active non-qualifie"
                            : "filter non-qualifie"
                    }
                    onClick={() =>
                        setFiltre("non_qualifie")
                    }
                >
                     Non qualifiés
                </button>


            </section>


            {/* ====================================== */}
            {/* CONTENU */}
            {/* ====================================== */}

            <section className="prospects-section">


                <div className="section-title">

                    <div>

                        <h2>
                            {filtre === "chaud" &&
                                "Prospects chauds"}

                            {filtre === "tiede" &&
                                "Prospects tièdes"}

                            {filtre === "froid" &&
                                "Prospects froids"}

                            {filtre === "non_qualifie" &&
                                "Prospects non qualifiés"}

                        </h2>


                        <p>
                            {prospects.length} prospect(s)
                        </p>

                    </div>
                    <section className="status-filters">

    <button
        className={
            statutFiltre === "tous"
                ? "status-filter active"
                : "status-filter"
        }
        onClick={() =>
            setStatutFiltre("tous")
        }
    >
        Tous
    </button>


    <button
        className={
            statutFiltre === "non_traite"
                ? "status-filter active non-traite"
                : "status-filter non-traite"
        }
        onClick={() =>
            setStatutFiltre("non_traite")
        }
    >
         Non traité
    </button>


    <button
        className={
            statutFiltre === "en_cours"
                ? "status-filter active en-cours"
                : "status-filter en-cours"
        }
        onClick={() =>
            setStatutFiltre("en_cours")
        }
    >
         En cours
    </button>


    <button
        className={
            statutFiltre === "traite"
                ? "status-filter active traite"
                : "status-filter traite"
        }
        onClick={() =>
            setStatutFiltre("traite")
        }
    >
         Traité
    </button>

</section>

                </div>


                {loading && (

                    <div className="loading">
                        Chargement...
                    </div>

                )}


                {error && (

                    <div className="error">
                        {error}
                    </div>

                )}


                {!loading &&
                !error &&
                prospects.length === 0 && (

                    <div className="empty">

                        Aucun prospect dans cette catégorie.

                    </div>

                )}


                {!loading &&
                !error &&
                prospects.length > 0 && (

                    <div className="prospect-grid">


                        {prospects.map(
                            (prospect) => (

                            <div
                                className="prospect-card"
                                key={prospect.id}
                            >


                                <div className="prospect-card-header">

                                    <div>

                                        <h3>

                                            {prospect.prenom}{" "}

                                            {prospect.nom}

                                        </h3>


                                        <span>

                                            {prospect.profession}

                                        </span>

                                    </div>


                                    <div className="score">

                                        {prospect.score}

                                    </div>

                                </div>


                                <div className="prospect-info">


                                    <div>

                                        <span>
                                             Téléphone
                                        </span>

                                        <strong>
                                            {prospect.telephone}
                                        </strong>

                                    </div>


                                    <div>

                                        <span>
                                             Âge
                                        </span>

                                        <strong>
                                            {prospect.age} ans
                                        </strong>

                                    </div>


                                    <div>

                                        <span>
                                             Qualification
                                        </span>

                                        <strong>
                                            {prospect.qualification}
                                        </strong>

                                    </div>


                                    <div>

                                        <span>
                                             Éligibilité
                                        </span>

                                        <strong>
                                            {prospect.eligibilite}
                                        </strong>

                                    </div>

                                <div>

    <span>
         Statut
    </span>

    <strong>

        {prospect.statut_conseiller === "non_traite" &&
            " Non traité"
        }

        {prospect.statut_conseiller === "en_cours" &&
            " En cours"
        }

        {prospect.statut_conseiller === "traite" &&
            " Traité"
        }

    </strong>

</div>

                                </div>


                                <button
                                    className="details-button"
                                    onClick={() =>
                                        consulterProspect(
                                            prospect
                                        )
                                    }
                                >

                                    Consulter 

                                </button>


                            </div>

                        ))}

                    </div>

                )}

            </section>


        </div>

    );

}


export default ConseillerDashboard;