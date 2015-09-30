module.exports = (grunt) ->
    grunt.initConfig(
        pkg: grunt.file.readJSON('package.json')
        coffee:
            files:
                src: ['src/js/**/*.coffee']
                dest: 'static/js/application_script.js',
        watch: {
            scripts: {
                files: ['src/js/**/*.coffee'],
                tasks: ['coffee'],
                options: {
                    spawn: false,
                },
            },
        },
    )

    grunt.loadNpmTasks('grunt-contrib-coffee')
    grunt.loadNpmTasks('grunt-contrib-watch')

    grunt.registerTask('default', ['watch'])
