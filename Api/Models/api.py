import flask
from forecast import compute_optimal_portfolio

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

  json = compute_optimal_portfolio(indexes,method,investment,months,risk_w)

  return json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
