using System;
using System.Collections.Generic;
using System.IO;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
namespace Api.Models {
  public class Persistence {
    private DbContext _context;
    public Persistence (FinContext context) {
      _context = context;
    }
    public List<string> readIndex (string attribute) {
      List<string> serie = new List<string> ();
      StreamWriter fout = new StreamWriter ("./data/" + attribute + ".csv", false);

      serie.Add (attribute);
      fout.WriteLine (attribute);
      using (var command = _context.Database.GetDbConnection ().CreateCommand ()) {
        command.CommandText = $"SELECT {attribute} FROM indici";
        _context.Database.OpenConnection ();
        using (var reader = command.ExecuteReader ()) {
          while (reader.Read ()) {
            fout.WriteLine (reader[attribute]);
            serie.Add (reader[attribute].ToString ());
          }
        }
      }
      fout.Close ();
      return serie;
    }

  }
}