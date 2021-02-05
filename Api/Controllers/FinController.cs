using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Api.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Api {
    public class Portfolio {
        public string horizon { get; set; }
        // public float S&P_500_INDEX {get;set;}
        // public float FTSE_MIB_INDEX {get;set;}
        // public float GOLD_SPOT_$_OZ {get;set;}
        // public float MSCI_EM {get;set;}
        // public float MSCI_EURO {get;set;}
        // public float All_Bonds_TR {get;set;}
        // public float U.S._Treasury {get;set;}

    }

    [Route ("api/[controller]")]
    [ApiController]
    public class FinController : ControllerBase {
        private readonly FinContext _context;

        private Persistence P;
        private string[] indices;
        public FinController (FinContext context) {
            _context = context;
            P = new Persistence (context);
            indices = new string[] { "SP_500", "FTSE_MIB", "GOLD_SPOT", "MSCI_EM", "MSCI_EURO", "All_Bonds", "US_Treasury" };

        }

        // GET: api/Fin
        [HttpGet]
        public string GetAllIndexes ([FromQuery] int investment = 1000, [FromQuery] int months = 6, [FromQuery] double risk_w = 0.5) {
            foreach (string attribute in indices) {
                var index = P.readIndex (attribute);
            }
            Forecast F = new Forecast ();
            // string res = "{";

            // res += F.forecastIndexes ("sarima", indices, investment, months, risk_w);
            // res += "}";
            string res = F.forecastRemote ("sarima", indices, investment, months, risk_w);
            Console.WriteLine (res);
            return res;
        }

        // GET: api/Fin/5
        [HttpGet ("{id}", Name = "GetFin")]
        public string GetFin (int id) {
            string res = "{";
            if (id > 7) id = 7;

            string attribute = indices[id];
            var index = P.readIndex (attribute);

            Forecast F = new Forecast ();
            res += F.forecastSARIMAindex (attribute);
            res += "}";

            return res;
        }

        // PUT: api/Fin/5
        // To protect from overposting attacks, enable the specific properties you want to bind to, for
        // more details, see https://go.microsoft.com/fwlink/?linkid=2123754.
        [HttpPut ("{id}")]
        public async Task<IActionResult> PutFin (int id, Fin fin) {
            if (id != fin.id) {
                return BadRequest ();
            }

            _context.Entry (fin).State = EntityState.Modified;

            try {
                await _context.SaveChangesAsync ();
            } catch (DbUpdateConcurrencyException) {
                if (!FinExists (id)) {
                    return NotFound ();
                } else {
                    throw;
                }
            }

            return NoContent ();
        }

        // POST: api/Fin
        // To protect from overposting attacks, enable the specific properties you want to bind to, for
        // more details, see https://go.microsoft.com/fwlink/?linkid=2123754.
        [HttpPost]
        public async Task<ActionResult<Fin>> PostFin (Fin fin) {
            _context.indici.Add (fin);
            await _context.SaveChangesAsync ();

            return CreatedAtAction ("GetFin", new { id = fin.id }, fin);
        }

        // DELETE: api/Fin/5
        [HttpDelete ("{id}")]
        public async Task<ActionResult<Fin>> DeleteFin (int id) {
            var fin = await _context.indici.FindAsync (id);
            if (fin == null) {
                return NotFound ();
            }

            _context.indici.Remove (fin);
            await _context.SaveChangesAsync ();

            return fin;
        }

        private bool FinExists (int id) {
            return _context.indici.Any (e => e.id == id);
        }
    }
}