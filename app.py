from flask import Flask, render_template, jsonify, request
import routeros_api
import config
import logging
import json

# Desativa logs excessivos do Flask no terminal
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

def get_api_connection():
    # Cria uma conexão nova e limpa para cada requisição
    connection = routeros_api.RouterOsApiPool(
        config.ROUTER_IP,
        username=config.USERNAME,
        password=config.PASSWORD,
        port=8728,
        plaintext_login=True
    )
    return connection

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/interfaces")
def interfaces():
    conn = None
    try:
        conn = get_api_connection()
        api = conn.get_api()
        resource = api.get_resource('/interface')
        data = resource.get()
        return jsonify(data)
    except Exception as e:
        print(f"Erro em /interfaces: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            try:
                conn.disconnect()
            except:
                pass

@app.route("/hosts")
def hosts():
    conn = None
    try:
        conn = get_api_connection()
        api = conn.get_api()
        resource = api.get_resource('/ip/arp')
        data = resource.get()
        return jsonify(data)
    except Exception as e:
        print(f"Erro em /hosts: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            try:
                conn.disconnect()
            except:
                pass

@app.route("/leases")
def leases():
    conn = None
    try:
        conn = get_api_connection()
        api = conn.get_api()
        resource = api.get_resource('/ip/dhcp-server/lease')
        data = resource.get()
        return jsonify(data)
    except Exception as e:
        print(f"Erro em /leases: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            try:
                conn.disconnect()
            except:
                pass

@app.route("/analysis")
def analysis():
    conn = None
    try:
        conn = get_api_connection()
        api = conn.get_api()
        
        # Coleta recursos do sistema
        res_resource = api.get_resource('/system/resource')
        identity_resource = api.get_resource('/system/identity')
        
        data = {
            "resource": res_resource.get()[0],
            "identity": identity_resource.get()[0]
        }
        return jsonify(data)
    except Exception as e:
        print(f"Erro em /analysis: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            try:
                conn.disconnect()
            except:
                pass

@app.route("/queues")
def queues():
    conn = None
    try:
        conn = get_api_connection()
        api = conn.get_api()
        resource = api.get_resource('/queue/simple')
        data = resource.get()
        return jsonify(data)
    except Exception as e:
        print(f"Erro em /queues: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            try:
                conn.disconnect()
            except:
                pass

@app.route("/set_speed", methods=["POST"])
def set_speed():
    from flask import request
    conn = None
    try:
        data = request.json
        queue_name = data.get("name")
        limit = data.get("limit") # Ex: "10M/10M"
        
        conn = get_api_connection()
        api = conn.get_api()
        queues = api.get_resource('/queue/simple')
        
        # Busca o ID da queue pelo nome
        q_original = queues.get(name=queue_name)
        if not q_original:
            return jsonify({"error": "Fila não encontrada"}), 404
            
        queues.set(id=q_original[0]['.id'], max_limit=limit)
        return jsonify({"success": True})
    except Exception as e:
        print(f"Erro ao alterar velocidade: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.disconnect()

@app.route("/boost_network", methods=["POST"])
def boost_network():
    conn = None
    try:
        conn = get_api_connection()
        api = conn.get_api()
        api.get_binary_resource('/').call('ip/dns/cache/flush')
        return jsonify({"success": True, "msg": "Boost ativado: Cache DNS limpo!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: conn.disconnect()

@app.route("/clear_arp", methods=["POST"])
def clear_arp():
    conn = None
    try:
        conn = get_api_connection()
        api = conn.get_api()
        arp = api.get_resource('/ip/arp')
        # Remove apenas entradas dinâmicas (recria a tabela e resolve conflitos)
        removidos = 0
        for item in arp.get():
            if item.get('dynamic') == 'true' or item.get('dynamic') == True:
                arp.remove(id=item['.id'])
                removidos += 1
        return jsonify({"success": True, "msg": f"Tabela ARP limpa! ({removidos} registros dinâmicos apagados)"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: conn.disconnect()

@app.route("/clear_leases", methods=["POST"])
def clear_leases():
    conn = None
    try:
        conn = get_api_connection()
        api = conn.get_api()
        leases = api.get_resource('/ip/dhcp-server/lease')
        removidos = 0
        for item in leases.get():
            if item.get('status') != 'bound':
                leases.remove(id=item['.id'])
                removidos += 1
        return jsonify({"success": True, "msg": f"Limpeza concluída! ({removidos} IPs liberados no DHCP)"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: conn.disconnect()

@app.route("/boost_jorge", methods=["POST"])
def boost_jorge():
    conn = None
    try:
        conn = get_api_connection()
        api = conn.get_api()
        queues = api.get_resource('/queue/simple')
        
        # Procura por Jorge, Sala do Jorge ou Porta 20
        all_queues = queues.get()
        target_id = None
        target_name = None
        
        for q in all_queues:
            name = q.get('name', '').upper()
            target = q.get('target', '').lower()
            if "JORGE" in name or "SALA DO JORGE" in name or "20" in name or "ETHER20" in target:
                target_id = q['.id']
                target_name = q['name']
                break
        
        if target_id:
            # Boost Máximo: 1000M/1000M
            queues.set(id=target_id, max_limit="1000M/1000M")
            return jsonify({"success": True, "msg": f"Boost aplicado na '{target_name}' (Porta 20)!"})
        else:
            return jsonify({"success": False, "error": "Fila do Jorge/Porta 20 não encontrada."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: conn.disconnect()

@app.route("/boost_all", methods=["POST"])
def boost_all():
    conn = None
    try:
        conn = get_api_connection()
        api = conn.get_api()
        queues = api.get_resource('/queue/simple')
        all_queues = queues.get()
        
        count = 0
        for q in all_queues:
            queues.set(id=q['.id'], max_limit="1000M/1000M")
            count += 1
            
        return jsonify({"success": True, "msg": f"Boost aplicado em todas as {count} filas!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: conn.disconnect()

@app.route("/ppp_active")
def ppp_active():
    conn = None
    try:
        conn = get_api_connection()
        api = conn.get_api()
        resource = api.get_resource('/ppp/active')
        return jsonify(resource.get())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: conn.disconnect()

@app.route("/hotspot_active")
def hotspot_active():
    conn = None
    try:
        conn = get_api_connection()
        api = conn.get_api()
        resource = api.get_resource('/ip/hotspot/active')
        return jsonify(resource.get())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: conn.disconnect()

@app.route("/run_speedtest")
def run_speedtest():
    import speedtest
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        ping = st.results.ping
        download = st.download() / 1024 / 1024 # Em Mbps
        upload = st.upload() / 1024 / 1024 # Em Mbps
        return jsonify({
            "success": True,
            "ping": round(ping, 1),
            "download": round(download, 2),
            "upload": round(upload, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/local_network")
def local_network():
    # Isso funciona no servidor Windows para ver dispositivos na rede do Modem Vivo.
    import subprocess
    try:
        resultado = subprocess.check_output(['arp', '-a']).decode('latin-1')
        dispositivos = []
        # Exemplo da tabela ARP no Windows:
        # Endereço IP           Endereço Físico       Tipo
        # 192.168.15.1          a4-91-b1-xx-xx-xx     dinâmico
        for linha in resultado.splitlines():
            partes = linha.split()
            if len(partes) >= 3 and partes[0].count('.') == 3:
                ip_local = partes[0]
                mac = partes[1]
                tipo = partes[2]
                dispositivos.append({
                    "address": ip_local,
                    "mac": mac,
                    "tipo": tipo
                })
        return jsonify(dispositivos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/mapa_dados")
def mapa_dados():
    import json
    import os
    caminho = os.path.join(os.path.dirname(__file__), "mapa_rede.json")
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return jsonify(dados)
    except Exception as e:
        return jsonify({"Erro": "Crie o arquivo mapa_rede.json com a estrutura correta."})

@app.route("/add_map_node", methods=["POST"])
def add_map_node():
    import json
    import os
    from flask import request
    try:
        data = request.json
        setor = data.get("setor", "Geral").strip()
        nome = data.get("nome").strip()
        ip = data.get("ip").strip()

        if not nome or not ip or not setor:
            return jsonify({"success": False, "error": "Preencha Setor, Nome e IP."})

        caminho = os.path.join(os.path.dirname(__file__), "mapa_rede.json")
        
        mapa_dados = {}
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                try:
                    mapa_dados = json.load(f)
                except:
                    pass
                    
        if setor not in mapa_dados:
            mapa_dados[setor] = []
            
        # Atualiza se existir ou cria novo
        atualizado = False
        for pessoa in mapa_dados[setor]:
            if pessoa["ip"] == ip or pessoa["nome"] == nome:
                pessoa["ip"] = ip
                pessoa["nome"] = nome
                atualizado = True
                break
                
        if not atualizado:
            mapa_dados[setor].append({"nome": nome, "ip": ip})
            
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(mapa_dados, f, indent=4, ensure_ascii=False)
            
        return jsonify({"success": True, "msg": f"{nome} ({ip}) adicionado em {setor}!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/logs")
def get_logs():
    conn = None
    try:
        count = request.args.get("count", 100, type=int)
        topics = request.args.get("topics", None)  # ex: "error,warning"
        conn = get_api_connection()
        api = conn.get_api()
        resource = api.get_resource('/log')
        if topics:
            data = resource.get(**{'topics': topics})
        else:
            data = resource.get()
        # Retorna os mais recentes primeiro, limitado
        return jsonify(data[-count:][::-1])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            try: conn.disconnect()
            except: pass

@app.route("/log_clear", methods=["POST"])
def log_clear():
    conn = None
    try:
        conn = get_api_connection()
        api = conn.get_api()
        api.get_binary_resource('/').call('log/print')
        # Limpa utilizando o recurso correto
        resource = api.get_resource('/log')
        logs = resource.get()
        for l in logs:
            try:
                resource.remove(id=l['.id'])
            except:
                pass
        return jsonify({"success": True, "msg": "Logs limpos!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            try: conn.disconnect()
            except: pass

@app.route("/terminal", methods=["POST"])
def terminal_exec():
    conn = None
    try:
        data = request.json
        cmd = data.get("command", "").strip()
        if not cmd:
            return jsonify({"error": "Comando vazio"}), 400

        # Converte ex: "ip address print" para ["/ip/address", "print"]
        parts = cmd.split()
        # Monta o caminho da API: ex ["ip", "address"] -> /ip/address
        if len(parts) < 2:
            return jsonify({"error": "Formato: <caminho> <ação> (ex: ip address print)"}), 400

        action = parts[-1]   # último item é a ação
        path_parts = parts[:-1]  # resto é o caminho
        api_path = '/' + '/'.join(path_parts)

        conn = get_api_connection()
        api = conn.get_api()
        resource = api.get_resource(api_path)

        if action == 'print':
            result = resource.get()
        elif action == 'remove':
            extra = data.get("args", {})
            resource.remove(**extra)
            result = [{"status": "OK - removido"}]
        elif action == 'add':
            extra = data.get("args", {})
            resource.add(**extra)
            result = [{"status": "OK - adicionado"}]
        else:
            # Tenta executar como call genérico
            result = api.get_binary_resource('/').call(cmd.replace(' ', '/'))
            result = [{"status": "Executado", "resposta": str(result)}]

        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn:
            try: conn.disconnect()
            except: pass

if __name__ == "__main__":
    print(f"\n==============================================")
    print(f"🚀 DASHBOARD ONLINE: http://localhost:8000")
    print(f"📡 CONECTADO EM: {config.ROUTER_IP}")
    print(f"==============================================\n")
    # threaded=False evita que o MikroTik receba multiplas conexões simultaneas do mesmo app
    app.run(host="0.0.0.0", port=8000, threaded=False)
