from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from rich import box
import textwrap
import readline

console=Console()

def input_multiline_with_blank_lines(prompt_text):
    """
    Fungsi untuk input multi-baris yang memungkinkan baris kosong
    dan memerlukan konfirmasi khusus untuk mengakhiri input
    """
    console.print(prompt_text)
    console.print("[dim]Tekan Enter 2x berturut-turut, lalu ketik 'done' untuk mengakhiri[/dim]")
    
    lines = []
    empty_line_count=0
    line_count=1
    
    while True:
        try:
            line = Prompt.ask(f"[dim]Baris {line_count}[/dim]", default="", show_default=False)
            
            if line.lower() == 'done':
                break
                
            if line == "":
                empty_line_count += 1
                if empty_line_count >= 2:
                    console.print("[yellow]⚠ Enter 2x berturut-turut. Ketik 'done' untuk benar-benar mengakhiri.[/yellow]")
            else:
                empty_line_count = 0
                
            lines.append(line)
            line_count += 1
   
        except KeyboardInterrupt:
            if Confirm.ask("\n[yellow]Batalkan input?[/yellow]"):
                return None
            else:
                console.print("[green]Melanjutkan input...[/green]")
                continue
    # Hapus baris kosong di akhir jika ada
    while lines and lines[-1] == "":
        lines.pop()
        
    return "\n".join(lines)
def main():
    console.clear()
    console.rule("[bold green]📱 WhatsApp Template Generator[/bold green]", style="green")
    # Input template panel
    console.print("\n")
    console.print(Panel.fit(
        "Masukkan [bold cyan]template pesan[/bold cyan] Anda.\n"
        "Gunakan kurung kurawal seperti [italic]{nama}[/italic] atau [italic]{produk}[/italic] untuk menulis kata yang mau diganti.\n"
        "Anda bisa memasukkan baris kosong dalam template.\n"
        "Untuk mengakhiri, tekan Enter 2x lalu ketik 'done'.",
        title="📝 Template Pesan", 
        border_style="blue", 
        padding=(1, 2)
    ))
    
    template=input_multiline_with_blank_lines("\nMulai mengetik template Anda:")
    if template is None:
        console.print("[yellow]Input template dibatalkan[/yellow]")
        return
        
    if not template.strip():
        console.print("[red]Template tidak boleh kosong[/red]")
        return
    # Tampilkan preview template
    console.print("\n")
    console.print(Panel.fit(
        template, 
        title="📋 Preview Template", 
        border_style="green", 
        padding=(1, 2)
    ))
    # Input kata ganti
    console.print("\n")
    console.print(Panel.fit(
        "Masukkan kata-kata yang akan diganti beserta tanda kurung kurawalnya.\n"
        "Pisahkan dengan koma (contoh: [italic]{nama},{produk},{harga}[/italic]).",
        title="🔍 Placeholder", 
        border_style="blue", 
        padding=(1, 2)
    ))
    while True:
        placeholders_input = Prompt.ask(
            "[bold]Masukkan placeholder[/bold]",
            default="", 
            show_default=False
        ).strip()
        if not placeholders_input:
            console.print("[red]⚠ Setidaknya satu placeholder diperlukan[/red]")
            continue
            
        placeholders = [p.strip() for p in placeholders_input.split(",") if p.strip()]
        # Validasi: cek apakah semua placeholder ada dalam template
        missing_placeholders = []
        for ph in placeholders:
            if ph not in template:
                missing_placeholders.append(ph)
                
        if missing_placeholders:
            console.print(f"[red]⚠ Placeholder berikut tidak ditemukan dalam template: {', '.join(missing_placeholders)}[/red]")
            if not Confirm.ask("Lanjutkan anyway?"):
                continue
                
        break
    
    # Input replacements
    console.print("\n")
    console.print(Panel.fit(
        f"Masukkan nilai pengganti untuk placeholder: [bold]{', '.join(placeholders)}[/bold]\n"
        "Format: pisahkan nilai dengan koma (contoh: [italic]Jaka,Humas[/italic])\n"
        "Ketik 'done' untuk menyelesaikan.",
        title="🔄 Data Pengganti", 
        border_style="blue", 
        padding=(1, 2)
    ))
    
    replacements = []
    example_shown = False
    
    while True:
        if not example_shown:
            console.print(f"[dim]Contoh: {','.join(['nilai1', 'nilai2'][:len(placeholders)])}[/dim]")
            example_shown = True
            
        line = Prompt.ask(
            f"[bold]Masukkan {len(placeholders)} nilai[/bold]",
            default="", 
            show_default=False
        ).strip()
        
        if line.lower() in ["selesai", "done", "exit", "quit"]:
            if not replacements:
                console.print("[red]⚠ Setidaknya satu set pengganti diperlukan[/red]")
                continue
            break
            
        items = [i.strip() for i in line.split(",")]
        
        if len(items) != len(placeholders):
            console.print(f"[red]⚠ Diperhatikan {len(placeholders)} nilai, tetapi {len(items)} diberikan[/red]")
            continue
            
        replacements.append(items)
        console.print(f"[green]✓ Data ke-{len(replacements)} ditambahkan[/green]")
    
    # Tampilkan ringkasan
    console.print("\n")
    summary_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    summary_table.add_column("No", style="dim", width=4)
    for ph in placeholders:
        summary_table.add_column(ph)
    
    for i, rep in enumerate(replacements, 1):
        summary_table.add_row(str(i), *rep)
    
    console.print(Panel.fit(
        summary_table,
        title="📊 Ringkasan Data",
        border_style="green",
        padding=(1, 1)
    ))
    
    # Konfirmasi sebelum generate
    if not Confirm.ask("\n[bold]Lanjutkan generate pesan?[/bold]"):
        console.print("[yellow]Operasi dibatalkan[/yellow]")
        return
    
    # Generate dan tampilkan hasil
    console.rule("[bold magenta]✨ Hasil Pesan[/bold magenta]", style="magenta")
    
    for i, rep in enumerate(replacements, 1):
        pesan = template
        for ph, val in zip(placeholders, rep):
            pesan = pesan.replace(ph, val)
        
        # === Output tanpa border ===
        console.print(f"[bold cyan]Pesan #{i}[/bold cyan]")
        console.print(pesan)  
        console.print(f"[dim]Replacements: {', '.join(f'{ph}={val}' for ph, val in zip(placeholders, rep))}[/dim]")
        console.print("-" * 50)  # pemisah antar pesan   
    console.rule("[bold green]✅ Selesai[/bold green]", style="green")
    console.print(f"Total {len(replacements)} pesan telah dihasilkan")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Program dihentikan oleh pengguna[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

