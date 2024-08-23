
// Styling
import "./Sidebar.scss"
import RmitLogo from "../../assets/img/rmit_logo.png";
import UNILogo from "../../assets/img/u&i_logo.jpg";
import Avatar from "../../assets/img/avatar.png";

export default function Sidebar() {
    return (
        <div className="sidebar">
            <div className="sidebar--top brand">
                <h2 className="brand__name">ADS</h2>
                <p>v1.2.4</p>
                <hr />
                <img className="brand__logo" src={RmitLogo} alt="RMIT Logo" />
                <img className="brand__logo" src={UNILogo} alt="U&I Logo" />
            </div>

            <div className="sidebar--bottom avatar">
                <img className="user-avatar" src={Avatar} alt="User avatar" />
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
                </svg>
            </div>
        </div>
    )
}