import os
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
from utils.db_operations import update_status, update_percentage, insert_result
from utils.directories import create_directories
from utils.download import download_images
from utils.ba_processing import process_images
from utils.geoserver_operations import upload_to_geoserver

app = Flask(__name__)

# Create a ThreadPoolExecutor to manage a pool of threads
executor = ThreadPoolExecutor(max_workers=4)

def process_burned_area(data, id_proses, threshold, sign):
    try:
        update_status(id_proses, "preparing")

        working_dir = create_directories(id_proses)
        update_percentage(id_proses, 10)

        update_status(id_proses, "processing")
        download_images(data, id_proses)
        update_percentage(id_proses, 30)

        data_dir = os.path.join(working_dir, 'data', data)
        output_dir = os.path.join(working_dir, 'output')

        dnbr_output = process_images(data_dir, output_dir, sign, threshold, id_proses)

        workspace = 'test'
        datastore = 'ba_' + id_proses
        style_name = 'burned_area'

        upload_response = upload_to_geoserver(dnbr_output, workspace, datastore, style_name)
        
        insert_result(id_proses, workspace, datastore)
        update_percentage(id_proses, 100)
        update_status(id_proses, "finished")

    except Exception as e:
        update_status(id_proses, f"failed: {str(e)}")

@app.route('/burnedarea', methods=['GET'])
def burned_area():
    data = request.args.get('data')
    id_proses = request.args.get('idproses')
    threshold = request.args.get('threshold')
    sign = request.args.get('sign')

    if not data or not sign or not threshold or not id_proses:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        # Submit the process_burned_area function to be executed in a separate thread
        executor.submit(process_burned_area, data, id_proses, threshold, sign)

        # Return immediately with a status response
        return jsonify({"message": "Processing started", "id_proses": id_proses, "status": "processing"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
