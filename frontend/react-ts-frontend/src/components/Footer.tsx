// src/components/Footer.tsx
import { Link } from 'react-router-dom';
import { FaFacebookF, FaTwitter, FaInstagram } from 'react-icons/fa';
import { MapPinIcon, EnvelopeIcon, PhoneIcon } from '@heroicons/react/24/outline';

export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-gray-400">
      {/* Top Section */}
      <div className="max-w-screen-xl mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <h3 className="text-white text-xl font-semibold mb-2">Hungry Cow</h3>
          <p className="leading-relaxed">
            Fresh, delicious meals delivered straight to your door. Join us and taste the difference!
          </p>
        </div>
        <div>
          <h3 className="text-white text-xl font-semibold mb-2">Navigate</h3>
          <ul className="space-y-2">
            {['/', '/menu', '/order', '/team'].map((path, i) => (
              <li key={i}>
                <Link to={path} className="hover:text-white transition">
                  {['Home','Menu','Order','Meet the Team'][i]}
                </Link>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h3 className="text-white text-xl font-semibold mb-2">Contact</h3>
          <ul className="space-y-3">
            <li className="flex items-center">
              <MapPinIcon className="h-5 w-5 text-red-500 mr-2" />
              123 Cow Lane, Farmville, CA
            </li>
            <li className="flex items-center">
              <EnvelopeIcon className="h-5 w-5 text-red-500 mr-2" />
              support@hungrycow.com
            </li>
            <li className="flex items-center">
              <PhoneIcon className="h-5 w-5 text-red-500 mr-2" />
              (555) 123-4567
            </li>
          </ul>
        </div>
      </div>

      {/* Divider */}
      <div className="border-t border-gray-800" />

      {/* Bottom Section */}
      <div className="max-w-screen-xl mx-auto px-6 py-4 flex flex-col md:flex-row items-center justify-between text-gray-500">
        <p className="text-sm">
          &copy; {year} Hungry Cow. All rights reserved.
        </p>
        <div className="flex space-x-4 mt-4 md:mt-0">
          {[FaFacebookF, FaTwitter, FaInstagram].map((Icon, idx) => (
            <Link key={idx} to="#" className="hover:text-white transition">
              <Icon className="h-5 w-5" />
            </Link>
          ))}
        </div>
      </div>
    </footer>
  );
}
