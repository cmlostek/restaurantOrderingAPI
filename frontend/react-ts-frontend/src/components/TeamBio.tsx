export default function TeamBio() {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Meet Our Team</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white shadow-md rounded-lg p-4">
          <img src="/images/team-member1.jpg" alt="Team Member 1" className="rounded-full w-32 h-32 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-center">John Doe</h2>
          <p className="text-gray-600 text-center">CEO & Founder</p>
        </div>
        <div className="bg-white shadow-md rounded-lg p-4">
          <img src="/images/team-member2.jpg" alt="Team Member 2" className="rounded-full w-32 h-32 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-center">Jane Smith</h2>
          <p className="text-gray-600 text-center">CTO</p>
        </div>
        {/* Add more team members as needed */}
      </div>
    </div>
  );
}