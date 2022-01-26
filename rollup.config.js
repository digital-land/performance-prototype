module.exports = [
  {
    input: `assets/javascripts/collapsible-section.js`,
    output: {
      file: `application/static/javascripts/collapsible-section.js`,
      format: 'iife',
    }
  },
  {
    input: `assets/javascripts/organisation-map-controller.js`,
    output: {
      file: `application/static/javascripts/organisation-map-controller.js`,
      format: 'iife',
    }
  },
  {
    input: `assets/javascripts/app-map.js`,
    output: {
      file: `application/static/javascripts/app-map.js`,
      format: 'iife',
    }
  }
];
