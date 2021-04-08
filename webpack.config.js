const path = require('path');
const glob = require('glob');

const entryArray = glob.sync('./front/src/**.js');

const entryObject = entryArray.reduce((acc, item) => {
    const name = item.replace('.js', '').replace('./front/src/', '');
    acc[name] = item;
    return acc;
  }, {}); 

module.exports = {
    mode: 'development',
    // entry: './front/index.js',
    // entry: {
    //     'index': './front/index.js',
    //     'index2': './front/index2.js'
    // },
    entry: entryObject,

    output: {
        path: path.resolve(__dirname, 'static/js'),
        filename: '[name].bundle.js'
    },

    resolve: {
        extensions: ['.js', '.jsx']
    },

    module: {
        rules: [
            { test: /\.js[x]?$/, use: 'babel-loader'}
        ]
    }
}