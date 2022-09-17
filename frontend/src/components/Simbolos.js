import React from "react";
import { useState, useEffect } from "react";

const SimbolosReport = () => {
  const [simbolos, setSimbolos] = useState([]);

  useEffect(() => {
    let isMounted = true;
    const getSimbolos = () => {
      const url = "http://localhost:5000/simbolos";
      fetch(url, {
        method: "GET", // or 'PUT'
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((res) => res.json())
        .catch((error) => console.error("Error:", error))
        .then((res) => {
          if (isMounted) setSimbolos(res.res);
        });
    };
    getSimbolos();
    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="main">
      <div className="d-flex justify-content-around">
        <h1>TABLA DE SIMBOLOS</h1>
      </div>
      <div className="d-flex justify-content-around">
        <table className="table table-hover">
          <thead>
            <tr>
              <th className="table-dark" scope="col">
                No.
              </th>
              <th className="table-primary" scope="col">
                ID
              </th>
              <th className="table-dark" scope="col">
                Tipo Símbolo
              </th>
              <th className="table-primary" scope="col">
                Tipo Dato
              </th>
              <th className="table-dark" scope="col">
                Ámbito
              </th>
              <th className="table-primary" scope="col">
                Fila
              </th>
              <th className="table-dark" scope="col">
                Columna
              </th>
            </tr>
          </thead>
          <tbody>
            {simbolos.map((simbolo, index) => (
              <tr key={index}>
                <th className="table-primary" scope="row">
                  {index + 1}
                </th>
                <td className="table-dark">{simbolo.identificador}</td>
                <td className="table-primary">{simbolo.tipo}</td>
                <td className="table-dark">{simbolo.tipoDato}</td>
                <td className="table-primary">{simbolo.ambito}</td>
                <td className="table-dark">{simbolo.linea}</td>
                <td className="table-primary">{simbolo.columna}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default SimbolosReport;
