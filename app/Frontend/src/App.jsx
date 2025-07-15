 function App() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-tr from-pink-400 via-blue-400 to-yellow-300 p-10">
      <div className="relative max-w-xs w-full bg-white rounded-2xl shadow-2xl p-8 transition-transform duration-500 hover:rotate-[8deg] hover:scale-110 hover:shadow-pink-400/50 overflow-hidden group">
        {/* Fun glowing ring */}
        <div className="absolute inset-0 bg-gradient-to-tr from-pink-400 via-blue-400 to-yellow-300 opacity-60 blur-2xl rounded-2xl -z-10 group-hover:opacity-90 transition-opacity"></div>
        <h1 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-700 via-pink-500 to-yellow-400 drop-shadow-lg mb-2 animate-pulse">
          Hello, Tailwind!
        </h1>
        <p className="text-gray-600 text-lg font-semibold mb-4">
          This card has gradients, glowing borders, 3D tilting, and even a trippy hover effect!
        </p>
        <button className="px-6 py-2 mt-2 bg-gradient-to-r from-blue-500 to-pink-500 text-white font-bold rounded-lg shadow-lg shadow-blue-300/50 hover:shadow-pink-300/60 transform hover:-translate-y-1 focus:outline-none focus:ring-4 focus:ring-pink-500 transition-all duration-300">
          Click Me
        </button>
      </div>
    </div>
  );
}
export default App;
