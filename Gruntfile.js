var uglify = require('uglify-es')
module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    root_dir: './src/main/webapp',
    pkg: grunt.file.readJSON('package.json'),

    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      build: {
        src: 'static/js/<%= "annotate" %>.js',
        dest: 'static/js/<%= "annotate" %>.min.js'
      }
    },
    cssmin: {
      options: {
        mergeIntoShorthands: false,
        roundingPrecision: -1
      },
      target: {
        files: [{
          expand: true,
          //cwd: 'static',
          src: ['./static/css/style.css', '/static/css/!*.min.css'],
          dest: './',
          ext: '.min.css'
        }]
      }
    },
    compress: {
      main: {
        options: {
          mode: 'gzip'
        },
        expand: true,
        src: [
        //'static/*.js',
         'static/css/*.css'],
        dest: './',
        //ext: '.gz.css'
        ext: '.gz.css'
      }
    },
    gzip: {
      options: { detail: true},
      index: {
        src: [
          //'static/index.html',
          'static/annotate.min.js',
          //'static/app.css'
        ],
      }
    }
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-uglify-es');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-gzip');
  grunt.loadNpmTasks('grunt-contrib-compress');

  // Default task(s).
  grunt.registerTask('default', ['uglify',
    //'cssmin','gzip',
    'compress'
    ]);
  //grunt.registerTask('default', ['gzip']);

};

/*
    watch:{
      js: {
        files: ['static/annotate.js',],
        tasks: ['concat', 'uglify', 'gzip'] // 実行させるタスク
      },
      css : {
        files: ['static/style.css'],
        tasks: ['cssmin'] // 実行させるタスク
      }
    },
*/
