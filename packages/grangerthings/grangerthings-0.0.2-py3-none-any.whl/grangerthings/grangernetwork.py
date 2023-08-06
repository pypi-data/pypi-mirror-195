class GrangerNetwork():
    def __init__(self, predictors):
        self.nodes = dict()
        self.weights = dict() 
        for predictor in predictors:
            if not predictor.name_to in self.nodes:
                self.nodes[predictor.name_to] = list()
                self.weights[predictor.name_to] = list()
            self.nodes[predictor.name_to].append(predictor)
            self.weights[predictor.name_to].append(predictor.weight())
        for node, weights in self.weights.items():
            sum_w = sum(weights)
            self.weights[node] = [w/sum_w for w in weights]
        
    def eat(self, node_to_symbol):
        for predictor_list in self.nodes.values():
            for predictor in predictor_list:
                predictor.eat(node_to_symbol[predictor.name_from])
    
    def predict(self, node_name):
        predictions = [p.predict() for p in self.nodes[node_name]]
        prediction = [0.0] * len(predictions[0])
        for i in range(len(predictions)):
            for j in range(len(predictions[i])):
                prediction[j] += self.weights[node_name][i] * predictions[i][j]
        return prediction
    
    def __str__(self):
        string = '' 
        for node in self.nodes:
            string += node + ':' + '\n'
            for i in range(len(self.nodes[node])):
                p = self.nodes[node][i]
                w = self.weights[node][i]
                string += '\t' + p.name_from + str(-(p.delay+1)) +' : '+ str(w) + '\n'
        return string
    
class GrangerPredictor():
    def __init__(self, predictor, name_from, name_to, delay, max_suffix = 100):
        self.predictor = predictor
        self.name_from = name_from 
        self.name_to = name_to
        self.delay = delay
        self.suffix = []
        self.max_suffix = max_suffix
        
    def eat(self, symbol):
        self.suffix.append(symbol)
        if len(self.suffix) > self.max_suffix:
            self.suffix = self.suffix[1:]
        
    def predict(self):
        if self.delay == 0:
            return self.predictor.predict(self.suffix)
        return self.predictor.predict(self.suffix[:-self.delay]) 
            
    def weight(self):
            return self.predictor.dependence_coefficient