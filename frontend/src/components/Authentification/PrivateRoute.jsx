import { Navigate } from "react-router-dom";

export default function PrivateRoute({ role, children }) {
    const saved = localStorage.getItem("user");
    const user = saved ? JSON.parse(saved) : null;

    if (!user || user.role !== role) {
        return <Navigate to="/authentification" replace />;
    }

    return children;
}