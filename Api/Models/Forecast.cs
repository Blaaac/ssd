using System;
using System.Drawing;
// using System.Drawing.;

namespace Api {
  public class Forecast {
    public Forecast () {

    }
    public string forecastIndexes (string method, string[] indexes, int investment, int months, double risk_w) {
      string res = "\"text\":\"";
      string json = "";
      string interpreter = "/home/ruben/anaconda3/bin/python";
      string environment = "opanalytics";
      int timeout = 10000;
      string portPrefix = "PORTFOLIO";
      PythonRunner PR = new PythonRunner (interpreter, environment, timeout);
      // Bitmap bmp = null;
      string attribute = indexes[0];
      string ix = string.Join (" ", indexes);
      try {
        string command = $"Models/forecast.py \"{ix} {method} {investment} {months} {risk_w} \"";
        string list = PR.runDosCommands (command);
        if (string.IsNullOrWhiteSpace (list)) {
          Console.WriteLine ("error in script call");
          goto lend;
          // return res;
        }
        string[] lines = list.Split (new [] { Environment.NewLine }, StringSplitOptions.None);
        string strBitMap = "";
        foreach (string s in lines) {
          if (s.StartsWith ("MAPE")) {
            // Console.Write (s);
            res += s;
          }
          if (s.StartsWith ("b'")) {
            Console.WriteLine ("image");
            strBitMap = s.Trim ();
            break;
          }
          if (s.StartsWith ("Actual")) {
            double fcast = Convert.ToDouble (s.Substring (s.LastIndexOf (" ")));
            Console.WriteLine (fcast);
          }
          if (s.StartsWith (portPrefix)) {
            Console.Write (s);
            json += s;
          }
        }
        json = "\"portfolio\":\"" + json.Substring (portPrefix.Length);
        json += "\"";

        //res += json;
        // Console.Write (strBitMap);
        // strBitMap = strBitMap.Substring (strBitMap.IndexOf ("b'"));
        res += "\"";
        res += "," + json;
        // res += ",\"img\":\"" + strBitMap + "\"";

        goto lend;

      } catch (Exception e) {
        Console.WriteLine (e.ToString ());
        goto lend;
      }

      lend:
        Console.WriteLine (json);

      return res; //json.Substring (portPrefix.Length);

    }

    public string forecastSARIMAindex (string attribute) {
      string res = "\"text\":\"";
      string interpreter = "/home/ruben/anaconda3/bin/python";
      string environment = "opanalytics";
      int timeout = 10000;
      PythonRunner PR = new PythonRunner (interpreter, environment, timeout);
      // Bitmap bmp = null;

      try {
        string command = $"Models/forecastStat.py {attribute}.csv";
        string list = PR.runDosCommands (command);
        if (string.IsNullOrWhiteSpace (list)) {
          Console.WriteLine ("error in script call");
          goto lend;
        }
        string[] lines = list.Split (new [] { Environment.NewLine }, StringSplitOptions.None);
        string strBitMap = "";
        foreach (string s in lines) {
          if (s.StartsWith ("MAPE")) {
            Console.Write (s);
            res += s;
          }
          if (s.StartsWith ("b'")) {
            Console.WriteLine ("aaaaaaaaaaaaaaaaaaa");
            strBitMap = s.Trim ();
            break;
          }
          if (s.StartsWith ("Actual")) {
            double fcast = Convert.ToDouble (s.Substring (s.LastIndexOf (" ")));
            Console.WriteLine (fcast);
          }
        }
        Console.Write (strBitMap);
        strBitMap = strBitMap.Substring (strBitMap.IndexOf ("b'"));
        res += "\",\"img\":\"" + strBitMap + "\"";
        // try{
        //   bmp = PR.FromPythonBase64String(strBitMap);
        // }
        // catch(Exception e){
        //   throw new Exception( "error occured while trying to create image: ", e);

        // }
        goto lend;

      } catch (Exception e) {
        Console.WriteLine (e.ToString ());
        goto lend;
      }
      lend:

        return res;

    }
  }
}