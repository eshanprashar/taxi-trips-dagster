const path = require('path');

module.exports = {
  mode: 'development',  // Use 'production' for production builds
  entry: './src/index.js',  // The entry point of your React app
  output: {
    path: path.resolve(__dirname, 'dist'),  // Output directory for the bundled files
    filename: 'main.js',  // Name of the bundled file
  },
  devServer: {
    static: './public',  // Serve static files from the 'public' directory
    hot: true,  // Enable hot reloading for development
    port: 8080,  // Port number for the development server
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,  // Handle JavaScript and JSX files
        exclude: /node_modules/,
        use: ['babel-loader'],  // Use Babel to transpile JS/JSX
      },
      {
        test: /\.css$/,  // Optional: If you're using CSS files, handle them here
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],  // Automatically resolve JS/JSX extensions
  },
};
