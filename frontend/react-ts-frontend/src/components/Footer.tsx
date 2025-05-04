export default function Footer() {
    return (
        <footer className="bg-white shadow-md">
        <div className="container mx-auto p-4">
            <p className="text-center text-gray-600">
            &copy; {new Date().getFullYear()} Hungry Cow. All rights reserved.
            </p>
        </div>
        </footer>
    );
}