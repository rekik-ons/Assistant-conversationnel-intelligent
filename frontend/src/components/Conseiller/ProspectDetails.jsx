import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import {
    modifierStatutProspect
} from "../../services/dashboardService";

import "./ProspectDetails.css";


function ProspectDetails() {

    const location = useLocation();
    const navigate = useNavigate();

    const prospect = location.state?.prospect;


    // ==========================================
    // STATUT DU PROSPECT
    // ==========================================

    const [statut, setStatut] = useState(
        prospect?.statut_conseiller || "non_traite"
    );

    const [loadingStatut, setLoadingStatut] = useState(false);


    // ==========================================
    // MODIFIER LE STATUT
    // ==========================================

    const changerStatut = async (nouveauStatut) => {

        try {

            setLoadingStatut(true);

            await modifierStatutProspect(
                prospect.id,
                nouveauStatut
            );

            setStatut(nouveauStatut);

        } catch (error) {

            console.error(
                "Erreur modification statut :",
                error
            );

            alert(
                "Impossible de modifier le statut du prospect."
            );

        } finally {

            setLoadingStatut(false);

        }
    };


    // ==========================================
    // PROSPECT ABSENT
    // ==========================================

    if (!prospect) {

        return (

            <div className="prospect-details-page">

                <div className="details-error">

                    <h2>
                        Prospect introuvable
                    </h2>

                    <p>
                        Les informations du prospect
                        n'ont pas été transmises.
                    </p>

                    <button
                        onClick={() =>
                            navigate("/conseiller")
                        }
                    >
                        Retour aux prospects
                    </button>

                </div>

            </div>
        );
    }


    return (

        <div className="prospect-details-page">


            {/* ================================= */}
            {/* HEADER */}
            {/* ================================= */}

            <header className="details-header">

                <div>

                    <h1>
                        Taysir Microfinance
                    </h1>

                    <p>
                        Détails du prospect
                    </p>

                </div>


                <button
                    className="back-button"
                    onClick={() =>
                        navigate("/conseiller")
                    }
                >
                    Retour
                </button>

            </header>


            <main className="details-container">


                {/* ================================= */}
                {/* INFORMATIONS PERSONNELLES */}
                {/* ================================= */}

                <section className="details-card">

                    <h2>
                         Informations personnelles
                    </h2>

                    <div className="details-grid">

                        <div>
                            <span>Nom</span>

                            <strong>
                                {prospect.nom || "-"}
                            </strong>
                        </div>


                        <div>
                            <span>Prénom</span>

                            <strong>
                                {prospect.prenom || "-"}
                            </strong>
                        </div>


                        <div>
                            <span>Téléphone</span>

                            <strong>
                                {prospect.telephone || "-"}
                            </strong>
                        </div>


                        <div>
                            <span>Âge</span>

                            <strong>
                                {prospect.age ?? "-"} ans
                            </strong>
                        </div>


                        <div>
                            <span>Profession</span>

                            <strong>
                                {prospect.profession || "-"}
                            </strong>
                        </div>


                        <div>
                            <span>Zone géographique</span>

                            <strong>
                                {prospect.zone_geographique || "-"}
                            </strong>
                        </div>

                    </div>

                </section>


                {/* ================================= */}
                {/* INFORMATIONS FINANCIÈRES */}
                {/* ================================= */}

                <section className="details-card">

                    <h2>
                         Informations financières
                    </h2>

                    <div className="details-grid">

                        <div>

                            <span>
                                Revenu mensuel
                            </span>

                            <strong>
                                {prospect.revenu ?? "-"} DT
                            </strong>

                        </div>


                        <div>

                            <span>
                                Charges mensuelles
                            </span>

                            <strong>
                                {prospect.charges ?? "-"} DT
                            </strong>

                        </div>


                        <div>

                            <span>
                                Capacité de remboursement
                            </span>

                            <strong>
                                {prospect.capacite_remboursement ?? "-"} DT
                            </strong>

                        </div>


                        <div>

                            <span>
                                Montant demandé
                            </span>

                            <strong>
                                {prospect.montant_demande ?? "-"} DT
                            </strong>

                        </div>

                    </div>

                </section>


                {/* ================================= */}
                {/* ÉVALUATION */}
                {/* ================================= */}

                <section className="details-card">

    <h2>Évaluation</h2>

    <div className="details-grid">

        <div>
            <span>Score</span>
            <strong>{prospect.score ?? 0} / 100</strong>
        </div>

        <div>
            <span>Qualification</span>
            <strong className={`qualification-badge ${prospect.qualification}`}>
                {prospect.qualification || "-"}
            </strong>
        </div>

        <div className="case-pleine">
    <span>Éligibilité</span>
    <strong className={prospect.eligibilite === "Éligible" ? "eligibilite-texte eligible" : "eligibilite-texte not-eligible"}>
        {prospect.eligibilite === "Éligible"
            ? "Ce prospect est éligible et peut être étudié par le conseiller."
            : "Ce prospect ne remplit pas les conditions d'éligibilité."}
    </strong>
</div>
    </div>

</section>
                


                {/* ================================= */}
                {/* TRAITEMENT DU PROSPECT */}
                {/* ================================= */}

                <section className="details-card traitement-card">

    <h2>Traitement du prospect</h2>

    <div className="details-grid">

        <div className="case-pleine">
            <span>Statut actuel</span>

            <strong className={`statut-texte ${statut}`}>
                {statut === "non_traite" && "Non traité"}
                {statut === "en_cours" && "En cours"}
                {statut === "traite" && "Traité"}
            </strong>
        </div>

    </div>

</section>


            </main>

        </div>
    );
}


export default ProspectDetails;