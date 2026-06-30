int main(){
    int x, y, z, w;

    // pre-conditions
    x = 0;
    y = 1;
    z = 0;
    w = 1;

    // loop body
    while(unknown()){
        if((x + y) % 2 == w){
            z = z + 1;
        }else{
            z = 0;
        }
        x = x + 1;
        y = y + 2;
        w = 1 - w;       
    }

    // post-condition
    if(x == 10){
        assert(z == x);
    }
    
}