import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    getDashboard,
    getRevenus,
    getProfils,
    getRecentProspects
} from "../../services/dashboardService";

import "./AdminDashboard.css";


function AdminDashboard() {

    const navigate = useNavigate();

    const [dashboard, setDashboard] = useState(null);
    const [revenus, setRevenus] = useState(null);
    const [profils, setProfils] = useState(null);
    const [recent, setRecent] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [message, setMessage] = useState(null);

    const afficherMessage = (type, texte) => {
    setMessage({ type, texte });
    setTimeout(() => setMessage(null), 3000);
};
    // ==========================================================
    // CHARGEMENT
    // ==========================================================

    useEffect(() => {

        chargerDashboard();

    }, []);


    const chargerDashboard = async () => {

        try {

            setLoading(true);
            setError("");

            const [
                dashboardData,
                revenusData,
                profilsData,
                recentData
            ] = await Promise.all([

                getDashboard(),
                getRevenus(),
                getProfils(),
                getRecentProspects()

            ]);

            setDashboard(dashboardData);
            setRevenus(revenusData);
            setProfils(profilsData);
            setRecent(recentData);

        } catch (err) {

            console.error(err);

            setError(
                "Impossible de charger les données du dashboard."
            );

        } finally {

            setLoading(false);

        }

    };

    // ==========================================================
// EXPORT CSV
// ==========================================================

const exporterCSV = async () => {
    try {
        const response = await fetch(
            "http://localhost:8000/prospects/export/csv"
        );

        if (!response.ok) {
            throw new Error("Erreur lors de l'export CSV");
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = url;
        link.download = "prospects.csv";

        document.body.appendChild(link);
        link.click();

        link.remove();
        window.URL.revokeObjectURL(url);

        afficherMessage("success", "Export réussi : prospects.csv a été téléchargé.");

    } catch (error) {
        console.error("Erreur export CSV :", error);
        afficherMessage("error", "Impossible d'exporter les prospects.");
    }
};
    // CONSULTER UN PROSPECT
    
    const consulterProspect = (prospect) => {

        navigate("/admin/prospect", {
            state: {
                prospect: prospect
            }
        });

    };


   // LOADING
    
    if (loading) {

    return (

        <div className="admin-page">

            <div className="admin-loading">
                Chargement du dashboard...
            </div>

        </div>

    );

}
    
    if (error) {

        return (

            <div className="admin-page">

                <div className="admin-error">

                    {error}

                    <button onClick={chargerDashboard}>
                        Réessayer
                    </button>

                </div>

            </div>

        );

    }


    return (

         <div className="admin-page">

       {message && (
    <div className={`alert-message ${message.type}`}>
        
        {message.texte}
    </div>
)}



            {/* HEADER */}
            
            <header className="admin-header">

                <div>

                    <h1>
                        Taysir Microfinance
                    </h1>

                    <p>
                        Espace administrateur
                    </p>

                </div>


                <div className="admin-header-actions">

    <button
        className="export-button"
        onClick={exporterCSV}
    >
        Exporter CSV
    </button>

    <button
        className="logout-button"
        onClick={() => {
            localStorage.removeItem("user");
            navigate("/authentification", { replace: true });
        }}
    >
        Se déconnecter
    </button>

</div>

            </header>


            

            {/* PROSPECTS RÉCENTS */}
            
            <section className="dashboard-section">


                <div className="section-header">

                    <h2>
                        Liste des prospects
                    </h2>

    

                </div>


                <div className="table-container">

                    <table>

                        <thead>

                            <tr>

                                <th>
                                    Nom
                                </th>

                                <th>
                                    Prénom
                                </th>

                                <th>
                                    Âge
                                </th>

                                <th>
                                    Profession
                                </th>

                                <th>
                                    Revenu
                                </th>

                                <th>
                                    Montant
                                </th>

                                <th>
                                    Score
                                </th>

                                <th>
                                    Qualification
                                </th>

                                <th>
                                    Éligibilité
                                </th>

                                <th>
                                    Action
                                </th>

                            </tr>

                        </thead>


                        <tbody>

                            {recent.length === 0 ? (

                                <tr>

                                    <td
                                        colSpan="10"
                                        className="empty"
                                    >
                                        Aucun prospect.
                                    </td>

                                </tr>

                            ) : (

                                recent.map(
                                    (prospect) => (

                                    <tr
                                        key={prospect.id}
                                    >

                                        <td>
                                            {prospect.nom}
                                        </td>

                                        <td>
                                            {prospect.prenom}
                                        </td>

                                        <td>
                                            {prospect.age}
                                        </td>

                                        <td>
                                            {prospect.profession}
                                        </td>

                                        <td>
                                            {prospect.revenu} DT
                                        </td>

                                        <td>
                                            {prospect.montant_demande} DT
                                        </td>

                                        <td>
                                            {prospect.score}
                                        </td>

                                        <td>

                                            <span
                                                className={
                                                    `qualification-badge ${
                                                        prospect.qualification
                                                    }`
                                                }
                                            >
                                                {
                                                    prospect.qualification
                                                }
                                            </span>

                                        </td>

                                        <td>

                                            <span
                                                className={
                                                    prospect.eligibilite ===
                                                    "Éligible"
                                                        ? "eligibility-badge eligible"
                                                        : "eligibility-badge not-eligible"
                                                }
                                            >

                                                {
                                                    prospect.eligibilite ||
                                                    "-"
                                                }

                                            </span>

                                        </td>


                                        <td>

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

                                        </td>

                                    </tr>

                                ))

                            )}

                        </tbody>

                    </table>

                </div>

            </section>


        </div>

    );

}


export default AdminDashboard;

