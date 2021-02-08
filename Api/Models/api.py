import flask
from forecast import compute_optimal_portfolio
import json
import os
from flask import request

app = flask.Flask(__name__)
# app.config["DEBUG"] = True


# route to perfom the optimization
@app.route('/api/portfolio', methods=['GET'])
def api_all():
  indexes = request.args.getlist("index")
  method = request.args.get("method",default = "sarima", type = str)
  months = request.args.get("months",default = 12, type = int)
  investment = request.args.get("investment",default = 1000, type = int)
  risk_w = request.args.get("risk_w",default = 0.5, type = int)

  json_out = compute_optimal_portfolio(indexes,method,investment,months,risk_w)
  path = str(os.environ.get("DATA_PATH","./data/"))
  try:
    with open(path+'portfolio.json', 'w', encoding='utf-8') as f:
      json.dump(json_out['portfolio'], f, ensure_ascii=False, indent=4)
  except:
    with open('portfolio.json', 'w', encoding='utf-8') as f:
      json.dump(json_out['portfolio'], f, ensure_ascii=False, indent=4)
  return json_out

if __name__ == '__main__':
  port = int(os.environ.get("PYTHONAPI_PORT", 5000))
  app.run(host='0.0.0.0', port=port)
