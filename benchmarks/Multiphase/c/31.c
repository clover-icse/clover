int main(){
    int x, z, w;

    // pre-conditions
    x = 0;
    assume(z > 53736239);
    w = 0;

    // loop body
    while(unknown()){
        if(x < z){
            w = w + 1;
        }else if(x % 2 == 0){
            w = w + 1;
        }else{
            w = w - 1;
        }
        x = x + 1;
    }

    // post-condition
    if(x > z){
        assert(w >= 0);
    }
    
}