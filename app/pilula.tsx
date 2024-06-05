class Pilula {
    inicio_pilula: Date;
    duracao_pilula: number;
    duracao_pausa: number;

    constructor(inicio_pilula: Date, duracao_pilula: number, duracao_pausa:number) {
        this.inicio_pilula = inicio_pilula;
        this.duracao_pilula = duracao_pilula;
        this.duracao_pausa = duracao_pausa;
    }

    diaDeTomarPilula(hoje: Date): boolean {
        let dias = Math.floor((hoje.getTime() - this.inicio_pilula.getTime()) / (1000 * 60 * 60 * 24));
        let dias_pilula = dias % (this.duracao_pilula + this.duracao_pausa);
        return dias_pilula < this.duracao_pilula;
    }

    getProximaPilula(): Pilula {
        let proxima_pilula = new Date(this.inicio_pilula.getTime() + (this.duracao_pilula + this.duracao_pausa) * 24 * 60 * 60 * 1000);
        return new Pilula(proxima_pilula, this.duracao_pilula, this.duracao_pausa);
    }

    getUltimoDiaPilula(): Date {
        let fim_pilula = new Date(this.inicio_pilula.getTime() + (this.duracao_pilula - 1) * 24 * 60 * 60 * 1000);
        return fim_pilula;
    }

    getInicioPausa(): Date {
        let fim_pilula = this.getUltimoDiaPilula();
        let inicio_pausa = new Date(fim_pilula.getTime() + 24 * 60 * 60 * 1000);
        return inicio_pausa;
    }

    getFimPausa(): Date {
        let inicio_pausa = this.getInicioPausa();
        let fim_pausa = new Date(inicio_pausa.getTime() + (this.duracao_pausa - 1) * 24 * 60 * 60 * 1000);
        return fim_pausa;
    }

    getInicioProximaPilula(): Date {
        let fim_pausa = this.getFimPausa();
        let inicio_proxima_pilula = new Date(fim_pausa.getTime() + 24 * 60 * 60 * 1000);
        return inicio_proxima_pilula;
    }


}

export default Pilula;