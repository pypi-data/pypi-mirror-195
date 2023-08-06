from numpy import ones, pi, cos, exp ,zeros
        
class mufcn:

    def __init__(self):
        self._radeg_ = pi/180.
        self._gamma_mu_ = 135.5

    def _load_data_(self,x,y,_int,_alpha,e=1):
        ''' 
        Must be called before activating _chisquare_
        x, y, e are numpy arrays
        e is always defined, 
        either provided by the caller 
        or default to np.ones(x.shape[0])
        _int is a compact model list
        _alpha is ditto
        '''
        if x.shape[0]!=y.shape[0]:
            raise ValueError('x, y have different lengths')
        else:
            self._x_ = x
            self._y_ = y
            self._alpha_ = _alpha
            self._int = _int
        if e.shape[0]==1:
            self._e_ = ones(x.shape[0])
        else:
            if e.shape[0]!=x.shape[0]:
                raise ValueError('x, e have different lengths')           
            else:
                self._e_ = e

    def _add_(self,x,*argv):
        '''
        used by self._chisquare_ 
        e.g. a blmg model with 
        argv will be a tuple of parameter values (val1,val2.val3,val4,val5,val6) at this iteration 
        _add_ reconstructs how to distribute these parameter values
        use to plot : 
          plt.errorbar(x,y,yerr=e)
          plt.plot(x,mumodel()._add_(x,val1,val2.val3,val4,val5,val6)                    
        '''  
        _da_flag_ = False
        f = zeros(x.shape[0])   
        p = argv # minuit stack of parameters
        k = -1
        for component,parkeys in self._int:   # this allows only for single run fits       
            p_comp = []
            for key in parkeys:
                if key == '~':
                    k += 1
                    p_comp.append(p[k]) # this is a parameter value from the stack
                else:
                    p_comp.append(eval(key[1:])) # this is a function string already referenced to the stack 
            # this loop assigns all component parameters from the stack
            # now use them in the component - handle of a mucomponents method
            if component == self.da:
                _da_flag = True
                da = p_comp[0]
            else:
                print('{}=self.da False'.format(component))
                f += component(x,*p_comp) # calculate the component
        if _da_flag:
            dada = da/self._alpha_
            f = ((2.+dada)*f-dada)/((2.+dada)-dada*f) # linearized correction 
        return f 

    def da(self,x,dalpha):
        '''
        fit component for linearized alpha correction
        x [mus], dalpha
        '''
        # the returned value will not be used, correction in _add_
        return zero(x.shape[0])

    def ml(self,x,asymmetry,field,phase,Lor_rate): 
        '''
        fit component for a precessing muon with Lorentzian decay, 
        x [mus], asymmetry, field [T], phase [degrees], Lor_rate [mus-1]
        '''
        # print('a={}, B={}, ph={}, lb={}'.format(asymmetry,field,phase,Lor_rate))
        return asymmetry*cos(2*pi*self._gamma_mu_*field*x+phase*self._radeg_)*exp(-x*Lor_rate)
   

    def _chisquare_(self,*argv):

        return sum(((self._add_(self._x_,*argv)-self._y_)/self._e_)**2)


