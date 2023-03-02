import NavBar from "./NavBar";

export default function Layout({ children }) {
    return (
        <>
            <div className="page-container">
                <NavBar />
                {children}
            </div>
        </>
    );
}