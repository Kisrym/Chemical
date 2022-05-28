class Chemical:
    def __init__(self, formula):
        self.formula = formula

    @staticmethod
    def round(value):
        """Arredonda o valor em ate 3 casas decimais.

        Args:
            value (float): Valor a ser arredondado

        Returns:
            float: Valor arrendondado
        """
        return float(f"{value:.3f}")

    def balance(self):
        """Retorna o balanceamento da equação química"""
        import regex
        
        def multiplicar_lista(lista):
            """
            Multiplica todos os elementos de uma lista.
            """
            n = 1
            if len(lista) > 1:
                for c in range(len(lista)):
                    n *= int(lista[c])
            else:
                n = lista[0]

            return str(n)
        
        def format(d1, d2):
            string_final = []
            
            for c in d1.keys():
                string_final.append(c)
                string_final.append("+")
            else:
                string_final.pop()
                string_final.append("=")
                
            for c in d2.keys():
                string_final.append(c)
                string_final.append("+")
            else:
                string_final.pop()
                
            for c in range(len(string_final)):
                if string_final[c][0] == '1':
                    string_final[c] = string_final[c][1:]
            
            return " ".join(string_final)
        
        while True:
            formula = []
            
            #? Separando os elementos
            self.formula = self.formula.split("=")
            for c in self.formula:
                formula.append(c.replace(" ", "").split("+"))

            #? Adicionando 1 caso não tenha
            for i in range(len(formula)):
                for c in formula[i]:
                    if c[0].isalpha():
                        formula[i][formula[i].index(c)] = "1" + c

            #? Transformando em dicionário
            d = {}
            for c in range(len(formula)):
                for v in formula[c]:
                    d[v] = []

            #? Adicionando os valores
            for key in d.keys():
                uau = regex.compile(r"\d?[A-Z][a-z]?\d*|\((?:[^()]*(?:\(.*\))?[^()]*)+\)\d+").findall(key)

                for i in uau:
                    chave = "".join([x for x in i if x.isnumeric() == False])
                    valor = [x for x in i if x.isnumeric()]

                    d[key].append({chave : valor})
            
            #? Verificando se dentro dos elementos tem uma lista vazia
            for key in d.keys():
                for indice in range(len(d[key])):
                    for key2 in d[key][indice].keys():
                        if len(d[key][indice][key2]) == 0: # se a lista for vazia vai adicionar 1
                            d[key][indice][key2] = ["1"]
                        
                        #? Adicionado o multiplicador geral
                        if key[0].isnumeric():
                            if indice > 0:
                                d[key][indice][key2].append(key[0])
            
            for key in d.keys():
                for c in d[key]:
                    for indice in range(len(d[key])):
                        for aa in d[key][indice].keys():
                            d[key][indice][aa] = multiplicar_lista(d[key][indice][aa])
            
            #? Dividindo o dicionário "d"
            divisor = 0
            for key in d.keys():
                chave_certa = self.formula[0].replace(" ","").split("+")[-1] if int(key[0]) != 1 else "1" + self.formula[0].replace(" ","").split("+")[-1]
                if key == chave_certa:
                    divisor += 1
                    break
                divisor += 1
            
            d1 = dict(list(d.items())[:divisor])
            d2 = dict(list(d.items())[divisor:])
            
            #? Criando a versão final dos dicionários, para não precisar editar o original
            d1_final = d1.copy()
            d2_final = d2.copy()
            
            #? dois métodos de correção
            correção = []
            correção_2 = 0
            
            for key_d1 in d1.keys():
                for key_d2 in d2.keys():
                    for c in range(len(d1[key_d1])):
                        for i in range(len(d2[key_d2])):
                            if d1[key_d1][c].keys() == d2[key_d2][i].keys():
                                if d1[key_d1][c] != d2[key_d2][i]:
                                    correção_2 += 1                     
                                    if int(list(d1[key_d1][c].values())[0]) > int(list(d2[key_d2][i].values())[0]):
                                        new_number = str(1 + int(key_d2[0]))
                                        d2_final[new_number + key_d2[1:]] = d2[key_d2]
                                        try: del d2_final[key_d2]
                                        except KeyError: continue
                                    
                                    elif int(list(d1[key_d1][c].values())[0]) < int(list(d2[key_d2][i].values())[0]):
                                        new_number = str(1 + int(key_d1[0]))
                                        d1_final[new_number + key_d1[1:]] = d1[key_d1]
                                        try: del d1_final[key_d1]
                                        except KeyError: continue
                                else:
                                    correção.append(True)
                                    
            if all(correção) == True and correção_2 == 0:
                return format(d1_final, d2_final)

            else:
                self.formula = format(d1_final, d2_final)

    def molar_mass(self):
        """Retorna a massa molar da molecula

        Returns:
            float: Aproximacao da massa molar da molecula
        """
        import regex
        self.formula = regex.compile(r'([A-Z][a-z]?)(\d*(?:(?:[\.|\,])\d+(?:\%)?)?)|(?:[\(|\[])([^()]*(?:(?:[\(|\[]).*(?:[\)|\]]))?[^()]*)(?:[\)|\]])(\d*(?:(?:[\.|\,]?)\d+(?:\%)?))').findall(self.formula)
        uau = 0
        if self.formula[0].isnumeric(): uau = self.formula[0]

        for c in range(len(self.formula)):
            if self.formula[c].isalpha():
                self.formula[c] = Chemical.element.get_by_id(self.formula[c])['massa_molar'].replace(",", ".")

            elif self.formula[c].isnumeric():
                self.formula[c] = int(self.formula[c])

        for c in range(len(self.formula)):
            if c == 0 and uau != 0: self.formula[c] = float(self.formula[c])
            elif c != 0:
                if type(self.formula[c]) == int:
                    self.formula[c-1] = self.formula[c-1]
                    self.formula[c-1] = float(self.formula[c-1]) * self.formula[c]
                
                elif float(self.formula[c]):
                    self.formula[c] = float(self.formula[c])

        self.formula = [x for x in self.formula if type(x) == float]
        if uau != 0:
            for c in range(len(self.formula)):
                if c == 0: continue
                self.formula[c] = self.formula[c] * float(uau)

            self.formula.pop(0)
        
        return sum([x for x in self.formula if type(x) == float])
        

    class element:
        def get_by_name(name):
            """Retorna as informacoes sobre determinado elemento.

            Args:
                name (str): Nome do elemento.

            Returns:
                dict: Informacoes sobre o elemento
            """
            from bs4 import BeautifulSoup
            from urllib.request import urlopen, Request
            from unidecode import unidecode
            import re
            
            if len(name) <= 2: raise ValueError("Nome de elemento inválido.")
            info = []

            try: html = urlopen(Request(f"https://www.tabelaperiodica.org/{unidecode(name.lower().strip())}/", headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}))
            except: raise ValueError("Elemento não existente")

            soup = BeautifulSoup(html.read(), 'lxml')
            texto = soup.find_all('p')[0].get_text('\n').replace(" ", "").split('\n')

            a = re.compile(r'[0-9,K\-°C]+')
            for c in range(len(texto)):
                try:
                    info.append(a.search(texto[c]).group())
                except AttributeError: continue

            if len(info) > 4:
                for c in range(len(info)-1):
                    if info[c] == ',': info.pop(c)
                info = info[:5]

            try:
                if 'K' not in info[2]: info.pop(2)
                if 'K' not in info[-1]: info[-1] = f"{info[-1]}K"
            except IndexError: pass

            while len(info) < 4:
                info.append(None)

            response = {"simbolo":soup.find_all('h1')[1].get_text(), "numero_atomico": info[0],"massa_molar": info[1],"fusao": info[2],"ebulicao": info[3], "nome":name.capitalize()}
            
            return response
        
        def get_by_id(id):
            """Retorna informacoes sobre determinado elemento pelo seu simbolo.

            Args:
            id (str): Simbolo do elemento

            Returns:
                dict: Informacoes sobre o elemento.
            """
            if len(id) > 2: raise ValueError("Id de elemento inválido.")
            e = ['H', 'Hidrogênio', 'He', 'Hélio', 'Li', 'Lítio', 'Be', 'Berílio', 'B', 'Boro', 'C', 'Carbono', 'N', 'Nitrogênio', 'O', 'Oxigênio', 'F', 'Flúor', 'Ne', 'Neônio', 'Na', 'Sódio', 'Mg', 'Magnésio', 'Al', 'Alumínio', 'Si', 'Silício', 'P', 'Fósforo', 'S', 'Enxofre', 'Cl', 'Cloro', 'Ar', 'Argônio', 'K', 'Potássio', 'Ca', 'Cálcio', 'Sc', 'Escândio', 'Ti', 'Titânio', 'V', 'Vanádio', 'Cr', 'Crômio', 'Mn', 'Manganês', 'Fe', 'Ferro', 'Co', 'Cobalto', 'Ni', 'Níquel', 'Cu', 'Cobre', 'Zn', 'Zinco', 'Ga', 'Gálio', 'Ge', 'Germânio', 'As', 'Arsênio', 'Se', 'Selênio', 'Br', 'Bromo', 'Kr', 'Criptônio', 'Rb', 'Rubídio', 'Sr', 'Estrôncio', 'Y', 'trio', 'Zr', 'Zircônio', 'Nb', 'Nióbio', 'Mo', 'Molibdênio', 'Tc', 'Tecnécio', 'Ru', 'Rutênio', 'Rh', 'Ródio', 'Pd', 'Paládio', 'Ag', 'Prata', 'Cd', 'Cádmio', 'In', 'ndio', 'Sn', 'Estanho', 'Sb', 'Antimônio', 'Te', 'Telúrio', 'I', 'Iodo', 'Xe', 'Xenônio', 'Cs', 'Césio', 'Ba', 'Bário', 'Hf', 'Háfnio', 'Ta', 'Tântalo', 'W', 'Tungstênio', 'Re', 'Rênio', 'Os', 'smio', 'Ir', 'Irídio', 'Pt', 'Platina', 'Au', 'Ouro', 'Hg', 'Mercúrio', 'Tl', 'Tálio', 'Pb', 'Chumbo', 'Bi', 'Bismuto', 'Po', 'Polônio', 'At', 'Astato', 'Rn', 'Radônio', 'Fr', 'Frâncio', 'Ra', 'Rádio', 'Rf', 'Rutherfórdio', 'Db', 'Dúbnio', 'Sg', 'Seabórgio', 'Bh', 'Bóhrio', 'Hs', 'Hássio', 'Mt', 'Meitnério', 'Ds', 'Darmstádtio', 'Rg', 'Roentgênio', 'Cn', 'Copernício', 'Nh', 'Nihônio', 'Fl', 'Fleróvio', 'Mc', 'Moscóvio', 'Lv', 'Livermório', 'Ts', 'Tennesso', 'Og', 'Oganessônio', 'Lantanídios', 'La', 'Lantânio', 'Ce', 'Cério', 'Pr', 'Praseodímio', 'Nd', 'Neodímio', 'Pm', 'Promécio', 'Sm', 'Samário', 'Eu', 'Európio', 'Gd', 'Gadolínio', 'Tb', 'Térbio', 'Dy', 'Disprósio', 'Ho', 'Hôlmio', 'Er', 'rbio', 'Tm', 'Túlio', 'Yb', 'Itérbio', 'Lu', 'Lutécio', 'Actinídios', 'Ac', 'Actínio', 'Th', 'Tório', 'Pa', 'Protactínio', 'U', 'Urânio', 'Np', 'Neptúnio', 'Pu', 'Plutônio', 'Am', 'Amerício', 'Cm', 'Cúrio', 'Bk', 'Berquélio', 'Cf', 'Califórnio', 'Es', 'Einstênio', 'Fm', 'Férmio', 'Md', 'Mendelévio', 'No', 'Nobélio', 'Lr', 'Laurêncio']
            try: response =  Chemical.element.get_by_name(e[e.index(id.capitalize())+1])
            except ValueError: raise ValueError("Elemento não existente.")
            response['nome'] = e[e.index(id.capitalize())+1]
            return response


a = Chemical("2K + Cl2 = KCl")

print(a.balance())