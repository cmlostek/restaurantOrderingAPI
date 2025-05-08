// src/components/Team.tsx

import React from 'react';
import { SparklesIcon } from '@heroicons/react/24/outline';

// imports for your assets (adjust paths)
import teamLogo from '../assets/hungry_cow.png';
import colePic from '../assets/cole.png';
import coleMood from '../assets/cole_moodboard.png';
import toyaPic from '../assets/toya2.png';
import toyaMood from '../assets/toya_moodboard2.png';
import daniellePic from '../assets/DanielleP.jpg';
import daniMood from '../assets/AboutDani.png';
import kristenPic from '../assets/kristenselfie.png';
import kristenMood from '../assets/kristen\'smood.png';

interface Member {
  id: string;
  name: string;
  role: string;
  photo: string;
  mood: string;
  bio: string;
}

const teamMembers: Member[] = [
  {
    id: 'cole',
    name: 'Cole Mlostek',
    role: 'Developer',
    photo: colePic,
    mood: coleMood,
    bio: 'Lead developer with a passion for project management, Python, bioinformatics, and data-driven insights.',
  },
  {
    id: 'toya',
    name: 'Toya Okey-Nwamara',
    role: 'Scrum Master',
    photo: toyaPic,
    mood: toyaMood,
    bio: 'Scrum Master overseeing agile processes, staff access control, and checkout system integrations.',
  },
  {
    id: 'danielle',
    name: 'Danielle Pottinger',
    role: 'Product Owner',
    photo: daniellePic,
    mood: daniMood,
    bio: 'Product Owner defining product vision, UX enhancements, and stakeholder communication.',
  },
  {
    id: 'kristen',
    name: 'Kristen Schroeter',
    role: 'Stakeholder',
    photo: kristenPic,
    mood: kristenMood,
    bio: 'Stakeholder driving staff login, access controls, and payment gateway features.',
  },
];

const Team: React.FC = () => {
  const [section, setSection] = React.useState<'bios' | 'vision'>('bios');

  return (
    <div className="container mx-auto px-6 py-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-center justify-between mb-12">
        <div className="flex items-center space-x-4 mb-6 md:mb-0">
          <img src={teamLogo} alt="Meet Our Team" className="w-12 h-12" />
          <h1 className="text-4xl font-extrabold">Meet Our Team</h1>
        </div>
        <div className="flex space-x-4">
          <button
            onClick={() => setSection('bios')}
            className={`px-4 py-2 rounded-md font-semibold transition ${
              section === 'bios'
                ? 'bg-red-600 text-white'
                : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-100'
            }`}
          >
            Team Bios
          </button>
          <button
            onClick={() => setSection('vision')}
            className={`px-4 py-2 rounded-md font-semibold transition ${
              section === 'vision'
                ? 'bg-red-600 text-white'
                : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-100'
            }`}
          >
            Team Vision
          </button>
        </div>
      </div>

      {/* Bios Grid */}
      {section === 'bios' && (
        <div className="grid gap-8 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
          {teamMembers.map((m) => (
            <div
              key={m.id}
              className="group relative bg-white rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition duration-300"
            >
              <div className="p-6 text-center">
                <h2 className="text-xl font-semibold mb-1">{m.name}</h2>
                <p className="text-red-600 mb-4">{m.role}</p>
                <img
                  src={m.photo}
                  alt={m.name}
                  className="mx-auto w-24 h-24 rounded-full object-cover mb-4"
                />
                <img
                  src={m.mood}
                  alt={`${m.name} moodboard`}
                  className="w-full h-32 object-cover rounded mb-4"
                />
              </div>
              <div className="absolute inset-0 bg-white bg-opacity-95 flex items-center justify-center p-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <p className="text-gray-800 text-sm text-center">{m.bio}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Enhanced Vision Section */}
      {section === 'vision' && (
        <section className="relative bg-red-50 rounded-lg shadow-lg p-12 overflow-hidden mb-12">
          <div className="absolute -top-16 -right-16 w-64 h-64 bg-red-600 opacity-20 rounded-full"></div>
          <div className="relative flex flex-col md:flex-row items-center md:items-start space-y-6 md:space-y-0 md:space-x-8">
            <SparklesIcon className="flex-shrink-0 h-16 w-16 text-red-600" />
            <div>
              <h2 className="text-3xl font-bold text-gray-800 mb-4">Our Mission Statement</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                Driven by curiosity and collaboration, our team is committed to building impactful,
                user-centered solutions that make a difference to the restaurant business. We combine
                diverse talents—from development and design to leadership and strategy—to create
                seamless digital experiences. Our mission is to innovate with purpose, empower each
                other, and deliver excellence in everything we do.
              </p>
            </div>
          </div>
        </section>
      )}

      {/* Footer / CTA */}
      <footer className="bg-gray-100 rounded-lg shadow-inner p-8 text-center mt-12">
        <h3 className="text-2xl font-semibold mb-4">Love What You See?</h3>
        <p className="text-gray-700 mb-6">
          Dive into our delicious menu and place an order to taste the magic yourself!
        </p>
        <a
          href="/menu"
          className="inline-block px-6 py-3 bg-red-600 text-white font-bold rounded-md hover:bg-red-700 transition"
        >
          View Full Menu
        </a>
      </footer>
    </div>
  );
};

export default Team;
