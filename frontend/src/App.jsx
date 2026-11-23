import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Chat from "./components/Chat/Chat";
import AdminDashboard from "./components/Admin/AdminDashboard";
import ConseillerDashboard from "./components/Conseiller/ConseillerDashboard";
import ProspectDetails from "./components/Conseiller/ProspectDetails";
import AdminProspectDetails from "./components/Admin/AdminProspectDetails";
import AdminConversation from "./components/Admin/AdminConversation";
import Authentification from "./components/Authentification/authentification";
import PrivateRoute from "./components/Authentification/PrivateRoute";

import "./App.css";


function App() {

    return (

        <BrowserRouter>

            <Routes>

                {/* Public */}
                <Route path="/" element={<Chat />} />
                <Route path="/authentification" element={<Authentification />} />

                {/* Administrateur */}
                <Route
                    path="/admin"
                    element={
                        <PrivateRoute role="administrateur">
                            <AdminDashboard />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/admin/prospect"
                    element={
                        <PrivateRoute role="administrateur">
                            <AdminProspectDetails />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/admin/conversation/:sessionId"
                    element={
                        <PrivateRoute role="administrateur">
                            <AdminConversation />
                        </PrivateRoute>
                    }
                />

                {/* Conseiller */}
                <Route
                    path="/conseiller"
                    element={
                        <PrivateRoute role="conseiller">
                            <ConseillerDashboard />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/conseiller/prospect"
                    element={
                        <PrivateRoute role="conseiller">
                            <ProspectDetails />
                        </PrivateRoute>
                    }
                />
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>

        </BrowserRouter>

    );
}

export default App;