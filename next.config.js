/** @type {import('next').NextConfig} */
module.exports = {
    images: {
      domains: ["images.unsplash.com", "images.pexels.com", "al-images-papers.s3.amazonaws.com","ik.imagekit.io"]
    },
    typescript: {
      // !! WARN !!
      // Dangerously allow production builds to successfully complete even if
      // your project has type errors.
      // !! WARN !!
      ignoreBuildErrors: true,
    },
  }