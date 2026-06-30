int main(){
    int x, y, z, w;

    // pre-conditions
    x = 0;
    y = 0;
    z = 0;
    w = 500;


    // loop body
    while(unknown()){
        if(x < 500){
            z = z + 1;
            w = w - 1;
        }else{
            z = z - 1;
            w = w + 1;
        }
        
        x = (x + 1) % 1000;
        y = y + 1;
    }

    // post-condition
    if(y == 2250){
        assert(z == w);
    }
    
}