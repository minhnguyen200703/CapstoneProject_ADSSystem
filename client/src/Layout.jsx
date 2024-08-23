import React from 'react';
import Sidebar from './components/sidebar/Sidebar';

// Styling
import "./Layout.scss";


export default function Layout({ children }) {
    return (
        <div className='layout'>
            <div className="layout--left">
                <Sidebar />
            </div>
            <div className="layout--right">
                {children}
            </div>
        </div>
    );
}