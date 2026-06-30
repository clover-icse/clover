int main(){
    int x, y, z, w;

    // pre-conditions
    x = 0;
    y = 0;
    z = 0;
    w = 0;

    // loop body
    while(unknown()){
        if(x < 1000){
            z = z + 1;
        }else{
            w = w + 1;
        }
        x = (x + 1) % 2000;
        y = y + 1;
        
    }

    // post-condition
    if(y == 1000000){
        assert(z == w);
    }
    
}