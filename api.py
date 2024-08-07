from flask import Flask, jsonify, request
from Media_Details_Extractors.watchseries import WatchSeriesExtractor
app = Flask(__name__)

@app.route('/VIDSRC-TO/Watch', methods=['GET'])
def get_f2cloud_watchseries():
    # Fetch Query Strings
    media_id = request.args.get('id')
    season = request.args.get('season')
    episode = request.args.get('episode')

    vse = WatchSeriesExtractor()
    m3u8_links = vse.get_streams(media_id,season,episode)
    return jsonify({"m3u8_links": m3u8_links, "subtitles": []})

@app.route('/WATCHSERIES/Search', methods=['GET'])
def search():
    # Fetch Query Strings
    vs =  WatchSeriesExtractor()
    query = request.args.get('query')
    results = vs.fetch_search_results(query)
    return jsonify(results)

@app.route('/WATCHSERIES/Trending', methods=['GET'])
def get_trending():
    vs =  WatchSeriesExtractor()
    results = vs.return_trending_json()
    return jsonify(results)

@app.route('/WATCHSERIES/Details', methods=['GET'])
def get_media_details():
    media_id = request.args.get('media_id')

    if not media_id:
        return jsonify("Need media_id")

    vs =  WatchSeriesExtractor()
    results = vs.fetch_media_details(media_id)
    return jsonify(results)

if __name__ == '__main__':
    app.run()