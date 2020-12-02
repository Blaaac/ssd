using Microsoft.EntityFrameworkCore;
namespace Api.Models
{
  public class FinContext : DbContext
  {
    public FinContext(DbContextOptions<FinContext> options)
    : base(options)
    {
    }
    public DbSet<Fin> indici { get; set; }
  }
}