import axios from "axios";

const API_URL = "http://127.0.0.1:8000";


// ==========================================================
// DASHBOARD GLOBAL
// ==========================================================

export const getDashboard = async () => {

    const response = await axios.get(
        `${API_URL}/dashboard`
    );

    return response.data;
};

export const getProspectsParStatut = async (statut) => {

    const response = await axios.get(
        `${API_URL}/dashboard/statut`,
        {
            params: {
                statut: statut
            }
        }
    );

    return response.data;
};
// ==========================================================
// QUALIFICATION
// ==========================================================

export const getQualification = async (qualification) => {

    const response = await axios.get(
        `${API_URL}/dashboard/qualification/${qualification}`
    );

    return response.data;
};


// ==========================================================
// ÉLIGIBILITÉ
// ==========================================================

export const getEligibilite = async (eligibilite) => {

    const response = await axios.get(
        `${API_URL}/dashboard/eligibilite`,
        {
            params: {
                eligibilite
            }
        }
    );

    return response.data;
};


// ==========================================================
// REVENUS
// ==========================================================

export const getRevenus = async () => {

    const response = await axios.get(
        `${API_URL}/dashboard/revenus`
    );

    return response.data;
};


// ==========================================================
// PROFILS
// ==========================================================

export const getProfils = async () => {

    const response = await axios.get(
        `${API_URL}/dashboard/profils`
    );

    return response.data;
};


// ==========================================================
// PROSPECTS RÉCENTS
// ==========================================================

export const getRecentProspects = async () => {

    const response = await axios.get(
        `${API_URL}/dashboard/recent`
    );

    return response.data;
};

export const getNonQualifies = async () => {

    const response = await axios.get(
        `${API_URL}/dashboard/non-qualifies`
    );

    return response.data;
};

export const modifierStatutProspect = async (
    prospectId,
    statut
) => {

    const response = await axios.patch(
        `${API_URL}/prospects/${prospectId}/statut`,
        null,
        {
            params: {
                statut: statut
            }
        }
    );

    return response.data;
};