echo "Running webpack"
npx webpack
echo "Webpack built"

# fswatch front/index.js | xargs -n1 sh -c ./script.sh